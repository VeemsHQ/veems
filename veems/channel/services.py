import logging

from django.db import transaction

from . import models

logger = logging.getLogger(__name__)


@transaction.atomic
def create_channel(*, name, user, is_selected=True, **kwargs):
    logger.info('Creating new channel: %s for user %s...', name, user.id)
    channel = models.Channel.objects.create(
        name=name,
        user=user,
        is_selected=is_selected,
        **kwargs,
    )
    if channel.is_selected:
        user.channels.exclude(id=channel.id).update(is_selected=False)
    return channel


def get_selected_channel_id(user):
    return user.channels.only('id').get(is_selected=True).id


def get_selected_channel(user):
    # TODO: test
    return user.channels.only('id').get(is_selected=True)


def update_channel(*, channel, **kwargs):
    logger.info('Updating channel %s...', channel.id)
    for field, val in kwargs.items():
        if field == 'user':
            raise RuntimeError('Updating of channel user is not permitted')
        setattr(channel, field, val)
    channel.save(update_fields=tuple(kwargs.keys()))
    if 'avatar_image' in kwargs:
        cached_attrs = (
            'avatar_image_small',
            'avatar_image_large',
        )
        for attr in cached_attrs:
            getattr(channel, attr).generate(force=True)
    if 'banner_image' in kwargs:
        cached_attrs = (
            'banner_image_small',
            'banner_image_large',
        )
        for attr in cached_attrs:
            getattr(channel, attr).generate(force=True)
    if channel.is_selected:
        channel.user.channels.exclude(id=channel.id).update(is_selected=False)
    channel.refresh_from_db()
    return channel


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
    logger.info('Setting avatar image for channel %s...', channel.id)
    channel.avatar_image = avatar_image
    channel.save(update_fields=('avatar_image',))
    return channel


def set_channel_banner_image(*, channel, banner_image):
    logger.info('Setting banner image for channel %s...', channel.id)
    channel.banner_image = banner_image
    channel.save(update_fields=('banner_image',))
    return channel
