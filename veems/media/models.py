from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField

from ..common.models import BaseModel
from .storage_backends import UploadStorage, MediaFormatStorage

TRANSCODE_JOB_CHOICES = (
    'created',
    'processing',
    'completed',
    'failed',
)

VIDEO_VISIBILITY_CHOICES = (
    'private',
    'public',
    'unlisted',
)


def _upload_file_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


def _mediaformat_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


class Upload(BaseModel):
    presigned_upload_url = models.URLField()
    media_type = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=_upload_file_upload_to, storage=UploadStorage
    )


class Video(BaseModel):
    upload = models.OneToOneField(Upload, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=10, choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES)
    )
    description = models.TextField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=1000), null=True)


class MediaFormat(BaseModel):
    """
    A format to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_mediaformat_upload_to, storage=MediaFormatStorage
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    framerate = models.IntegerField(null=True)  # 30
    name = models.CharField(max_length=30, null=False)  # 240p
    ext = models.CharField(max_length=4, null=False)  # webm
    audio_codec = models.CharField(max_length=50, null=True)  # mp4a.40.2
    video_codec = models.CharField(max_length=50, null=True)  # vp9
    container = models.CharField(max_length=30, null=True)
    filesize = models.IntegerField()  # bytes


class TranscodeJob(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10, choices=tuple((c, c) for c in TRANSCODE_JOB_CHOICES)
    )
    started_on = models.DateTimeField(db_index=True, null=True)
    ended_on = models.DateTimeField(db_index=True, null=True)
    # TODO: failure context
