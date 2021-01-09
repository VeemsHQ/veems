import logging

from . import models

logger = logging.getLogger(__name__)


def create_channel(*, name, user, **kwargs):
    # TODO: test with img
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
