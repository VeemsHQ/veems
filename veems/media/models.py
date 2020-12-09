from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField

from ..common.models import BaseModel
from . import storage_backends

TRANSCODE_JOB_CHOICES = (
    'created',
    'processing',
    'completed',
    'failed',
)

# TODO: default to 'draft'.
VIDEO_VISIBILITY_CHOICES = (
    'private',
    'public',
    'unlisted',
)


def _upload_file_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


def _mediafile_upload_to(instance, filename):
    return f'{instance.id}{Path(filename).suffix}'


def _media_file_thumbnail_upload_to(instance, filename):
    # TODO: test
    return f'{instance.media_file.id}/{instance.id}{Path(filename).suffix}'


class Upload(BaseModel):
    presigned_upload_url = models.URLField()
    media_type = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=_upload_file_upload_to,
        storage=storage_backends.UploadStorage
    )


class Video(BaseModel):
    upload = models.OneToOneField(Upload, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=10, choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES)
    )
    description = models.TextField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=1000), null=True)


class MediaFile(BaseModel):
    """
    A format to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_mediafile_upload_to,
        storage=storage_backends.MediaFileStorage
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    framerate = models.IntegerField(null=True)  # 30
    duration = models.IntegerField(null=True)  # secs
    name = models.CharField(max_length=30, null=False)  # 240p
    ext = models.CharField(max_length=4, null=False)
    audio_codec = models.CharField(max_length=50, null=True)
    video_codec = models.CharField(max_length=50, null=True)
    container = models.CharField(max_length=30, null=True)
    file_size = models.IntegerField()  # bytes
    # TODO: add duration seconds,


class MediaFileThumbnail(BaseModel):
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_media_file_thumbnail_upload_to,
        storage=storage_backends.MediaFileThumbnailStorage
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    # TODO: validate no .
    ext = models.CharField(max_length=4, null=False)


class TranscodeJob(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10, choices=tuple((c, c) for c in TRANSCODE_JOB_CHOICES)
    )
    started_on = models.DateTimeField(db_index=True, null=True)
    ended_on = models.DateTimeField(db_index=True, null=True)
    failure_context = models.TextField(null=True)
    # TODO: store failure context

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.profile} {self.status}>'
        )
