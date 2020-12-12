import tempfile
from pathlib import Path

from django.utils import timezone
from ffprobe import FFProbe
from django.conf import settings

from .transcoder_executor import ffmpeg as transcode_executor
from . import transcoder_profiles
from .. import models
from ...celery import async_task


def create_transcodes(video_id):
    video = models.Video.objects.get(id=video_id)
    upload = video.upload
    uploaded_file = tempfile.NamedTemporaryFile(
        suffix=Path(upload.file.name).name
    )
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
            task_transcode.delay(video.id, transcode_job_id)


def _get_applicable_transcode_profiles(video_path):
    metadata = FFProbe(str(video_path))
    ffprobe_stream = metadata.video[0]
    should_apply = []
    for profile_cls in transcoder_profiles.PROFILES:
        if _transcode_profile_does_apply(
            profile_cls=profile_cls, ffprobe_stream=ffprobe_stream
        ):
            should_apply.append(profile_cls)
    return should_apply


def _transcode_profile_does_apply(profile_cls, ffprobe_stream):
    if (
        profile_cls.required_aspect_ratio
        and ffprobe_stream.display_aspect_ratio !=
        profile_cls.required_aspect_ratio
    ):
        return False
    if (
        profile_cls.width > int(ffprobe_stream.width)
        and profile_cls.height > int(ffprobe_stream.height)
    ):
        return False
    if not (
        profile_cls.min_framerate <= ffprobe_stream.framerate <=
        profile_cls.max_framerate
    ):
        return False
    return True


def _mark_transcode_job_processing(transcode_job):
    transcode_job.status = 'processing'
    transcode_job.started_on = timezone.now()
    transcode_job.save()


@async_task()
def task_transcode(video_id, transcode_job_id):
    video = models.Video.objects.get(id=video_id)
    upload = video.upload
    transcode_job = models.TranscodeJob.objects.get(id=transcode_job_id)
    _mark_transcode_job_processing(transcode_job=transcode_job)
    uploaded_file = tempfile.NamedTemporaryFile(
        suffix=Path(upload.file.name).name, delete=False
    )
    with uploaded_file as file_:
        file_.write(upload.file.read())
        transcode_executor.transcode(
            transcode_job=transcode_job,
            source_file_path=Path(uploaded_file.name)
        )
