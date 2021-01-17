from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.templatetags.static import static
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ..common.models import BaseModel
from ..channel.models import Channel
from . import storage_backends

STORAGE_BACKEND = storage_backends.MediaStorage
UPLOAD_CHOICES = (
    'draft',
    'completed',
)
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


def _video_rendition_upload_to(instance, filename):
    video_rendition = instance
    video_id = video_rendition.video_id
    return (
        f'videos/{video_id}/renditions/{video_rendition.id}/rendition/'
        f'{video_rendition.id}{Path(filename).suffix}'
    )


def _video_rendition_playlist_file_upload_to(instance, filename):
    video_rendition = instance
    video_id = video_rendition.video_id
    return (
        f'videos/{video_id}/renditions/{video_rendition.id}/'
        f'playlists/{video_rendition.id}_{instance.name}.m3u8'
    )


def _video_rendition_segment_upload_to(instance, filename):
    segment = instance
    video_rendition = segment.video_rendition
    video_rendition_id = segment.video_rendition_id
    video_id = video_rendition.video_id

    return (
        f'videos/{video_id}/renditions/{video_rendition_id}/'
        f'segments/{segment.segment_number}.ts'
    )


def _video_thumbnail_image_upload_to(instance, filename):
    video = instance
    return f'videos/{video.id}/thumbnails/{video.id}{Path(filename).suffix}'


def _video_rendition_thumbnail_upload_to(instance, filename):
    thumbnail = instance
    video_rendition = thumbnail.video_rendition
    video_rendition_id = thumbnail.video_rendition_id
    video_id = video_rendition.video_id
    return (
        f'videos/{video_id}/renditions/{video_rendition_id}/'
        f'thumbnails/{thumbnail.id}{Path(filename).suffix}'
    )


class Upload(BaseModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='uploads'
    )
    presigned_upload_url = models.URLField(max_length=1000)
    media_type = models.CharField(max_length=500)
    file = models.FileField(
        upload_to=_upload_file_upload_to, storage=STORAGE_BACKEND
    )
    status = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in UPLOAD_CHOICES),
        default='draft',
        db_index=True,
    )

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.channel_id} {self.status}>'
        )


class Video(BaseModel):
    upload = models.OneToOneField(
        Upload, null=True, on_delete=models.CASCADE, blank=True
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='videos'
    )
    title = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES),
        db_index=True,
        default='public',
    )
    is_viewable = models.BooleanField(default=False, db_index=True)
    description = models.TextField(max_length=5000)
    tags = ArrayField(models.CharField(max_length=1000), null=True)
    framerate = models.IntegerField(null=True)
    duration = models.IntegerField(null=True, default=0)
    default_thumbnail_image = models.ImageField(
        upload_to=_video_thumbnail_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
    )
    default_thumbnail_image_small = ImageSpecField(
        source='default_thumbnail_image',
        processors=[ResizeToFit(480, 270)],
        format='JPEG',
        options={'quality': 70},
    )
    default_thumbnail_image_large = ImageSpecField(
        source='default_thumbnail_image',
        processors=[ResizeToFit(720, 404)],
        format='JPEG',
        options={'quality': 85},
    )

    @property
    def default_thumbnail_image_small_url(self):
        if not self.default_thumbnail_image_small:
            return static(
                'images/player/error-video-processing-simple-480p.png'
            )
        return self.default_thumbnail_image_small.url

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.channel_id} {self.title}>'
        )


class VideoRendition(BaseModel):
    """
    A format/rendition to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=_video_rendition_upload_to, storage=STORAGE_BACKEND
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
        upload_to=_video_rendition_playlist_file_upload_to,
        storage=STORAGE_BACKEND,
    )

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.name} {self.width} {self.height}>'
        )


class VideoRenditionSegment(BaseModel):
    video_rendition = models.ForeignKey(
        VideoRendition, on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=_video_rendition_segment_upload_to,
        storage=storage_backends.MediaStoragePublic,
    )
    segment_number = models.IntegerField()

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.video_rendition_id} {self.segment_number}>'
        )

    class Meta:
        unique_together = ('video_rendition', 'segment_number')


class VideoRenditionThumbnail(BaseModel):
    video_rendition = models.ForeignKey(
        VideoRendition, on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=_video_rendition_thumbnail_upload_to, storage=STORAGE_BACKEND
    )
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    time_offset_secs = models.IntegerField(null=True)
    ext = models.CharField(max_length=4, null=False)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.width} {self.height}>'
        )


class TranscodeJob(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in TRANSCODE_JOB_CHOICES),
        db_index=True,
    )
    started_on = models.DateTimeField(db_index=True, null=True)
    ended_on = models.DateTimeField(db_index=True, null=True)
    failure_context = models.TextField(null=True)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.profile} {self.status}>'
        )
