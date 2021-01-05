from pathlib import Path

from django.db import models
from django.contrib.auth import get_user_model

from ..common.models import BaseModel
from ..common import validators
from ..media import storage_backends

STORAGE_BACKEND = storage_backends.MediaStorage


def _channel_avatar_image_upload_to(instance, filename):
    channel = instance
    return f'channels/profile_images/{channel.id}{Path(filename).suffix}'


def _channel_banner_image_upload_to(instance, filename):
    channel = instance
    return f'channels/banner_images/{channel.id}{Path(filename).suffix}'


class Channel(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='channels'
    )
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=5000)
    sync_videos_interested = models.BooleanField()
    language = models.CharField(
        max_length=2, validators=(validators.validate_language,), default=None
    )
    avatar_image = models.ImageField(
        upload_to=_channel_avatar_image_upload_to, storage=STORAGE_BACKEND,
        null=True,
    )
    banner_image = models.ImageField(
        upload_to=_channel_banner_image_upload_to, storage=STORAGE_BACKEND,
        null=True,
    )

    # TODO: add default images

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} {self.name}>'
