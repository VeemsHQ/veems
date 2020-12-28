import logging

from . import models

logger = logging.getLogger(__name__)


def create_channel(*, name, user, description, sync_videos_interested):
    logger.info('Creating new channel: %s for user %s', name, user.id)
    return models.Channel.objects.create(
        name=name,
        user=user,
        description=description,
        sync_videos_interested=sync_videos_interested,
    )


def get_channel(id):
    return models.Channel.objects.get(id=id)
