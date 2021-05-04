from pathlib import Path
from django.templatetags.static import static

from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..common.models import BaseModel
from ..media import storage_backends
from ..common import validators
from .. import images

STORAGE_BACKEND = storage_backends.MediaStorage


def _channel_avatar_image_upload_to(instance, filename):
    channel = instance
    return (
        f'channels/avatar-images/original/{channel.id}{Path(filename).suffix}'
    )


def _channel_banner_image_upload_to(instance, filename):
    channel = instance
    return f'channels/banner-images/{channel.id}{Path(filename).suffix}'


def _validate_minimum_size_avatar_image(value):
    return validators.validate_minimum_size(width=98, height=98)(value)


def _validate_minimum_size_banner_image(value):
    return validators.validate_minimum_size(width=2048, height=1152)(value)


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
    sync_videos_interested = models.BooleanField(db_index=True, default=True)
    language = models.CharField(
        max_length=2, validators=(validators.validate_language,), default=None
    )
    avatar_image = models.ImageField(
        verbose_name='Avatar Image',
        upload_to=_channel_avatar_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
        validators=(_validate_minimum_size_avatar_image,),
    )
    avatar_image_small = ImageSpecField(
        source='avatar_image',
        processors=[ResizeToFill(44, 44)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    avatar_image_large = ImageSpecField(
        source='avatar_image',
        processors=[ResizeToFill(88, 88)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    banner_image = models.ImageField(
        verbose_name='Banner Image',
        upload_to=_channel_banner_image_upload_to,
        storage=STORAGE_BACKEND,
        null=True,
        blank=True,
        validators=(_validate_minimum_size_banner_image,),
    )
    banner_image_large = ImageSpecField(
        source='banner_image',
        processors=[SmartResize(2560, 1440)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
    )
    banner_image_small = ImageSpecField(
        source='banner_image',
        processors=[SmartResize(1360, 765)],
        format='JPEG',
        options={'quality': 90, 'optimize': True},
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


@receiver(pre_save, sender=Channel)
def channel_pre_save_callback(sender, instance, *args, **kwargs):
    if instance.banner_image:
        instance.banner_image = images.remove_exif_data(
            image_file=instance.banner_image.file
        )
    if instance.avatar_image:
        instance.avatar_image = images.remove_exif_data(
            image_file=instance.avatar_image.file
        )
