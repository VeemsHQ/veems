import logging
import re
from pathlib import Path

import boto3
from django.conf import settings

from . import models
from .transcoder import manager as transcode_manager
from ..celery import async_task
from . import services

ONE_DAY_IN_SECS = 86400
logger = logging.getLogger(__name__)


def _get_presigned_upload_url(*, upload, filename):
    s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
    bucket_name = upload.file.field.storage.bucket_name
    object_name = models._upload_file_upload_to(
        instance=upload, filename=filename
    )
    response = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name,
        },
        ExpiresIn=ONE_DAY_IN_SECS,
    )
    return response, object_name


def prepare(*, user, filename, channel_id):
    logger.info('Preparing new upload for user %s...', user.id)
    channel = models.Channel.objects.get(id=channel_id, user=user)
    upload = models.Upload.objects.create(media_type='video', channel=channel)
    upload.presigned_upload_url, upload.file.name = _get_presigned_upload_url(
        upload=upload, filename=filename
    )
    upload.save()
    title = _default_video_title_from_filename(filename)
    video = services.create_video(upload=upload, title=title)
    logger.info(
        'Done preparing upload for user %s, draft video %s', user.id, video.id
    )
    return upload, video


def _default_video_title_from_filename(filename):
    value = re.sub(r'[^\w\s-]', ' ', Path(filename).stem, re.IGNORECASE)
    value = re.sub(r'[-_]+', ' ', value)
    return re.sub(r' {2,}', ' ', value)


@async_task()
def complete(upload_id):
    logger.info('Completing Upload...')
    upload = models.Upload.objects.get(id=upload_id)
    if upload.status == 'completed':
        logger.warning('Upload %s already completed, exiting...', upload.id)
        return None
    transcode_manager.create_transcodes(video_id=upload.video.id)
    _mark_upload_completed(upload)
    logger.info('Completed Upload, transcoding started')


def _mark_upload_completed(upload):
    upload.status = 'completed'
    upload.save(update_fields=('status',))
