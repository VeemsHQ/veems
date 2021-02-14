from pathlib import Path
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.templatetags.static import static
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToCover
from django.contrib.auth import get_user_model

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
    'draft',
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


def _video_default_thumbnail_image_upload_to(instance, filename):
    video = instance
    return (
        f'videos/{video.id}/'
        f'thumbnails/default/{video.id}{Path(filename).suffix}'
    )


def _video_custom_thumbnail_image_upload_to(instance, filename):
    video = instance
    return (
        f'videos/{video.id}/'
        f'thumbnails/custom/{video.id}{Path(filename).suffix}'
    )


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
    presigned_upload_url = models.URLField(
        max_length=1000, null=True, blank=True
    )
    media_type = models.CharField(max_length=500)
    file = models.FileField(
        upload_to=_upload_file_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
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
    title = models.CharField(max_length=500, null=True, blank=True)
    visibility = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in VIDEO_VISIBILITY_CHOICES),
        db_index=True,
        default='public',
    )
    is_viewable = models.BooleanField(default=False, db_index=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    tags = ArrayField(models.TextField(max_length=1000), null=True, blank=True)
    framerate = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, default=0)
    # Custom thumb is user uploaded
    custom_thumbnail_image = models.ImageField(
        upload_to=_video_custom_thumbnail_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
    )
    custom_thumbnail_image_small = ImageSpecField(
        source='custom_thumbnail_image',
        # TODO: cover and fit and crop
        processors=[ResizeToCover(320, 240,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    custom_thumbnail_image_medium = ImageSpecField(
        source='custom_thumbnail_image',
        processors=[ResizeToCover(640, 360,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    custom_thumbnail_image_large = ImageSpecField(
        source='custom_thumbnail_image',
        processors=[ResizeToCover(1280, 720,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    # Default thumb is picked from the video frames
    default_thumbnail_image = models.ImageField(
        upload_to=_video_default_thumbnail_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
    )
    default_thumbnail_image_small = ImageSpecField(
        source='default_thumbnail_image',
        processors=[ResizeToCover(320, 240,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    default_thumbnail_image_medium = ImageSpecField(
        source='default_thumbnail_image',
        processors=[ResizeToCover(640, 360,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    default_thumbnail_image_large = ImageSpecField(
        source='default_thumbnail_image',
        processors=[ResizeToCover(1280, 720,)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.channel_id} {self.title}>'
        )

    @property
    def thumbnail_image_small_url(self):
        if not self.custom_thumbnail_image_small:
            return self.default_thumbnail_image_small_url
        return self.custom_thumbnail_image_small.url

    @property
    def thumbnail_image_medium_url(self):
        if not self.custom_thumbnail_image_medium:
            return self.default_thumbnail_image_medium_url
        return self.custom_thumbnail_image_medium.url

    @property
    def thumbnail_image_large_url(self):
        if not self.custom_thumbnail_image_large:
            return self.default_thumbnail_image_large_url
        return self.custom_thumbnail_image_large.url

    @property
    def default_thumbnail_image_small_url(self):
        if not self.default_thumbnail_image_small:
            return static(
                'images/player/error-video-processing-simple-480p.png'
            )
        return self.default_thumbnail_image_small.url

    @property
    def default_thumbnail_image_medium_url(self):
        if not self.default_thumbnail_image_medium:
            return static(
                'images/player/error-video-processing-simple-480p.png'
            )
        return self.default_thumbnail_image_medium.url

    @property
    def default_thumbnail_image_large_url(self):
        if not self.default_thumbnail_image_large:
            return static(
                'images/player/error-video-processing-simple-480p.png'
            )
        return self.default_thumbnail_image_large.url


class VideoRendition(BaseModel):
    """
    A format/rendition to be linked to a Video.

    Either a piece of Audio/Video/Audio+Video.
    """

    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='renditions'
    )
    file = models.FileField(
        upload_to=_video_rendition_upload_to,
        storage=STORAGE_BACKEND,
    )
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    framerate = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=30, null=False)
    ext = models.CharField(max_length=4, null=False)
    audio_codec = models.CharField(max_length=50, null=True, blank=True)
    video_codec = models.CharField(max_length=50, null=True, blank=True)
    container = models.CharField(max_length=30, null=True, blank=True)
    codecs_string = models.CharField(max_length=100, null=True, blank=True)
    file_size = models.IntegerField()
    metadata = models.JSONField(null=True, blank=True)
    playlist_file = models.FileField(
        upload_to=_video_rendition_playlist_file_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f'<{self.__class__.__name__} '
            f'{self.id} {self.name} {self.width} {self.height}>'
        )


class VideoRenditionSegment(BaseModel):
    video_rendition = models.ForeignKey(
        VideoRendition,
        on_delete=models.CASCADE,
        related_name='rendition_segments',
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
        VideoRendition,
        on_delete=models.CASCADE,
        related_name='rendition_thumbnails',
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
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='transcode_jobs',
    )
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in TRANSCODE_JOB_CHOICES),
        db_index=True,
    )
    started_on = models.DateTimeField(db_index=True, null=True, blank=True)
    ended_on = models.DateTimeField(db_index=True, null=True, blank=True)
    failure_context = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} '
            f'{self.profile} {self.status}>'
        )


class VideoLikeDislike(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='likedislikes'
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='likedislikes'
    )
    is_like = models.BooleanField(db_index=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return (
            f'<{self.__class__.__name__} {self.id} {self.video_id} '
            f'{self.is_like}>'
        )
