from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField

from ..common.models import BaseModel
from . import storage_backends

STORAGE_BACKEND = storage_backends.MediaStorage
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
    upload = instance
    return f'uploads/{upload.id}{Path(filename).suffix}'


def _media_file_upload_to(instance, filename):
    media_file = instance
    return f'media_files/{media_file.id}{Path(filename).suffix}'


def _media_file_playlist_file_upload_to(instance, filename):
    media_file = instance
    return f'manifests/media_files/{media_file.id}_{instance.name}.m3u8'


def _video_playlist_file_upload_to(instance, filename):
    video = instance
    return f'manifests/videos/{video.id}_master.m3u8'


def _media_file_segment_upload_to(instance, filename):
    return (
        'media_files/segments/'
        f'{instance.media_file.id}/{instance.segment_number}.ts'
    )


def _media_file_thumbnail_upload_to(instance, filename):
    return (
        f'media_files/thumbnails/{instance.media_file.id}/'
        f'{instance.id}{Path(filename).suffix}'
    )


class Upload(BaseModel):
    presigned_upload_url = models.URLField()
    media_type = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=_upload_file_upload_to, storage=STORAGE_BACKEND
    )


class Video(BaseModel):
    upload = models.OneToOneField(Upload, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES),
    )
    description = models.TextField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=1000), null=True)
    playlist_file = models.FileField(
        upload_to=_video_playlist_file_upload_to,
        storage=STORAGE_BACKEND,
        null=True
    )


class MediaFile(BaseModel):
    """
    A format/rendition to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_media_file_upload_to, storage=STORAGE_BACKEND
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    framerate = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    name = models.CharField(max_length=30, null=False)
    ext = models.CharField(max_length=4, null=False)
    audio_codec = models.CharField(max_length=50, null=True)
    video_codec = models.CharField(max_length=50, null=True)
    container = models.CharField(max_length=30, null=True)
    codecs_string = models.CharField(max_length=100, null=True)
    file_size = models.IntegerField()
    metadata = models.JSONField(null=True)
    playlist_file = models.FileField(
        upload_to=_media_file_playlist_file_upload_to,
        storage=STORAGE_BACKEND
    )


class MediaFileSegment(BaseModel):
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_media_file_segment_upload_to, storage=STORAGE_BACKEND
    )
    segment_number = models.IntegerField()

    class Meta:
        unique_together = ('media_file', 'segment_number')


class MediaFileThumbnail(BaseModel):
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_media_file_thumbnail_upload_to, storage=STORAGE_BACKEND
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    time_offset_secs = models.IntegerField(null=True)
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

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.profile} {self.status}>'
        )
