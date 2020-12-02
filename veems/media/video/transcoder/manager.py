import tempfile
from pathlib import Path

from celery import shared_task
from django.utils import timezone

from .transcoder_executor import ffmpeg as transcode_executor
from . import transcoder_profiles
from ... import models

# TODO: move to settings.py
EXECUTOR = 'ffmpeg'


def handle_upload_complete(upload_id):
    upload = models.Upload.objects.get(id=upload_id)
    for profile_cls in transcoder_profiles.PROFILES:
        transcode_job_id = models.TranscodeJob.objects.create(
            upload=upload,
            profile=profile_cls.name,
            executor=EXECUTOR,
            status='created',
        ).id
        task_transcode.delay(upload.id, transcode_job_id)


def _mark_transcode_job_processing(transcode_job):
    transcode_job.status = 'processing'
    transcode_job.started_on = timezone.now()
    transcode_job.save()


@shared_task()
def task_transcode(upload_id, transcode_job_id):
    upload = models.Upload.objects.get(id=upload_id)
    transcode_job = models.TranscodeJob.objects.get(id=transcode_job_id)
    _mark_transcode_job_processing(transcode_job=transcode_job)
    uploaded_file = tempfile.NamedTemporaryFile(suffix=upload.file.name,
    )
    with uploaded_file as file_:
        file_.write(upload.file.read())
        transcode_executor.transcode(
            transcode_job=transcode_job, source_file_path=Path(uploaded_file.name)
        )
