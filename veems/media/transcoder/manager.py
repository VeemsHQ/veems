import tempfile
import logging
from pathlib import Path

from django.conf import settings
from celery import chord

from .transcoder_executor import ffmpeg as transcode_executor
from . import transcoder_profiles
from .. import models
from ...celery import async_task
from .. import services

logger = logging.getLogger(__name__)


def create_transcodes(video_id):
    logger.info('Creating transcodes for video %s', video_id)
    video = models.Video.objects.get(id=video_id)
    upload = video.upload
    uploaded_file = tempfile.NamedTemporaryFile(
        suffix=Path(upload.file.name).name
    )
    task_transcode_args = []
    with uploaded_file as file_:
        file_.write(upload.file.read())
        profiles = _get_applicable_transcode_profiles(file_.name)
        for profile_cls in profiles:
            transcode_job_id = models.TranscodeJob.objects.create(
                video=video,
                profile=profile_cls.name,
                executor=settings.ACTIVE_EXECUTOR,
                status='created',
            ).id
            task_transcode_args.append((video.id, transcode_job_id))
    tasks = [
        task_transcode.s(video_id=video_id, transcode_job_id=transcode_job_id)
        for video_id, transcode_job_id in task_transcode_args
    ]
    logger.info(
        'Created %s transcode tasks for video %s', len(tasks), video_id
    )
    callback = task_on_all_transcodes_completed.s(video.id)
    async_result = chord(tasks, callback).delay()
    return async_result


@async_task()
def task_on_all_transcodes_completed(task_results, video_id):
    if not task_results:
        logger.warning('Not all transcodes successful for Video %s', video_id)
    logger.info('Transcodes completes callback executed')


@async_task()
def task_transcode(*args, video_id, transcode_job_id):
    logger.info('Task transcode started %s %s', video_id, transcode_job_id)
    video = models.Video.objects.get(id=video_id)
    upload = video.upload
    transcode_job = models.TranscodeJob.objects.get(id=transcode_job_id)
    if transcode_job.status == 'completed':
        logger.warning(
            'Task transcode exited, already completed '
            'previously %s %s', video_id, transcode_job_id
        )
        return True
    services.mark_transcode_job_processing(transcode_job=transcode_job)
    uploaded_file = tempfile.NamedTemporaryFile(
        suffix=Path(upload.file.name).name, delete=False
    )
    with uploaded_file as file_:
        file_.write(upload.file.read())
        transcode_executor.transcode(
            transcode_job=transcode_job,
            source_file_path=Path(uploaded_file.name)
        )
    logger.info('Task transcode completed %s %s', video_id, transcode_job_id)
    return True


def _get_applicable_transcode_profiles(video_path):
    metadata_summary = services.get_metadata(video_path)['summary']
    should_apply = []
    for profile_cls in transcoder_profiles.PROFILES:
        if _transcode_profile_does_apply(
            profile_cls=profile_cls, metadata_summary=metadata_summary
        ):
            should_apply.append(profile_cls)
    return should_apply


def _transcode_profile_does_apply(profile_cls, metadata_summary):
    if (
        profile_cls.required_aspect_ratio
        and metadata_summary['video_aspect_ratio'] !=
        profile_cls.required_aspect_ratio
    ):
        return False
    if (
        profile_cls.width > metadata_summary['width']
        and profile_cls.height > metadata_summary['height']
    ):
        return False
    if not (
        profile_cls.min_framerate <= metadata_summary['framerate'] <=
        profile_cls.max_framerate
    ):
        return False
    return True
