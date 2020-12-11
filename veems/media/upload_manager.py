import logging

import boto3

from . import models
from .transcoder import manager as transcode_manager
from ..celery import async_task

ONE_DAY_IN_SECS = 86400
logger = logging.getLogger(__name__)


def _get_presigned_upload_url(*, upload, filename):
    # s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
    s3 = boto3.client('s3')
    bucket_name = upload.file.field.storage.bucket_name
    object_name = models._upload_file_upload_to(
        instance=upload, filename=filename
    )
    response = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        },
        ExpiresIn=ONE_DAY_IN_SECS,
    )
    return response


def prepare(filename):
    upload = models.Upload.objects.create(media_type='video')
    upload.presigned_upload_url = _get_presigned_upload_url(
        upload=upload, filename=filename
    )
    upload.save()
    video = models.Video.objects.create(
        upload=upload,
        visibility='draft',
    )
    return upload, video


@async_task()
def complete(upload_id):
    logger.info('Completing Upload...')
    video_id = models.Video.objects.get(upload_id=upload_id).id
    transcode_manager.create_transcodes(video_id=video_id)
    logger.info('Completed Upload, transcoding started')
