from pathlib import Path
from django.templatetags.static import static

from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from ..common.models import BaseModel
from ..common import validators
from ..media import storage_backends

STORAGE_BACKEND = storage_backends.MediaStorage


def _channel_avatar_image_upload_to(instance, filename):
    channel = instance
    return (
        f'channels/avatar-images/original/{channel.id}{Path(filename).suffix}'
    )


def _channel_banner_image_upload_to(instance, filename):
    channel = instance
    return f'channels/banner-images/{channel.id}{Path(filename).suffix}'


class Channel(BaseModel):
    _DEFAULT_AVATAR_PATH = 'images/defaults/avatar.svg'
    _DEFAULT_BANNER_PATH = 'images/defaults/channel-banner-image.png'
    _DEFAULT_BANNER_LARGE_PATH = (
        'images/defaults/channel-banner-image-large.png'
    )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='channels'
    )
    name = models.CharField(max_length=60, db_index=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    sync_videos_interested = models.BooleanField(db_index=True)
    language = models.CharField(
        max_length=2, validators=(validators.validate_language,), default=None
    )
    avatar_image = models.ImageField(
        upload_to=_channel_avatar_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True, blank=True,
    )
    avatar_image_small = ImageSpecField(
        source='avatar_image',
        processors=[ResizeToFill(44, 44)],
        format='JPEG',
        options={'quality': 70},
    )
    avatar_image_large = ImageSpecField(
        source='avatar_image',
        processors=[ResizeToFill(88, 88)],
        format='JPEG',
        options={'quality': 85},
    )
    banner_image = models.ImageField(
        upload_to=_channel_banner_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
    )
    banner_image_large = ImageSpecField(
        source='banner_image',
        processors=[ResizeToFit(2560, 1440)],
        format='JPEG',
        options={'quality': 85},
    )
    banner_image_small = ImageSpecField(
        source='banner_image',
        processors=[ResizeToFit(1360, 765)],
        format='JPEG',
        options={'quality': 70},
    )

    # User may have many Channels, but only one may be selected
    # at any one time.
    is_selected = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} {self.name}>'

    @property
    def avatar_image_url(self):
        if not self.avatar_image:
            return static(self._DEFAULT_AVATAR_PATH)
        return self.avatar_image.url

    @property
    def avatar_image_small_url(self):
        if not self.avatar_image_small:
            return static(self._DEFAULT_AVATAR_PATH)
        return self.avatar_image_small.url

    @property
    def avatar_image_large_url(self):
        if not self.avatar_image_large:
            return static(self._DEFAULT_AVATAR_PATH)
        return self.avatar_image_large.url

    @property
    def banner_image_large_url(self):
        if not self.banner_image_large:
            return static(self._DEFAULT_BANNER_LARGE_PATH)
        return self.banner_image_large.url

    @property
    def banner_image_small_url(self):
        if not self.banner_image_small:
            return static(self._DEFAULT_BANNER_PATH)
        return self.banner_image_small.url
