import logging

from . import models

logger = logging.getLogger(__name__)


def create_channel(*, name, user, **kwargs):
    logger.info('Creating new channel: %s for user %s', name, user.id)
    return models.Channel.objects.create(
        name=name,
        user=user,
        **kwargs,
    )


def get_channel(id, user_id=None):
    filters = {'id': id}
    if user_id:
        filters['user_id'] = user_id
    return models.Channel.objects.get(**filters)


def get_channels(user_id=None):
    filters = {}
    if user_id:
        filters['user_id'] = user_id
    return models.Channel.objects.filter(**filters)


def set_channel_avatar_image(*, channel, avatar_image):
    channel.avatar_image = avatar_image
    channel.save()
    return channel


def set_channel_banner_image(*, channel, banner_image):
    channel.banner_image = banner_image
    channel.save()
    return channel
