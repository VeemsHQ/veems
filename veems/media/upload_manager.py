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


def _get_presigned_upload_url(*, upload, filename, num_parts):
    bucket_name = upload.file.field.storage.bucket_name
    object_name = models._upload_file_upload_to(
        instance=upload, filename=filename
    )
    provider = _provider()
    response = provider.create_multipart_upload(
        Bucket=bucket_name, Key=object_name
    )
    provider_upload_id = response['UploadId']
    urls = []
    for part_number in range(num_parts):
        part_number = part_number + 1
        url = provider.generate_presigned_url(
            ClientMethod='upload_part',
            Params={
                'Bucket': bucket_name,
                'UploadId': provider_upload_id,
                'Key': object_name,
                'PartNumber': part_number,
            },
            ExpiresIn=ONE_DAY_IN_SECS,
        )
        urls.append(url)
    return provider_upload_id, urls, object_name


def prepare(*, user, filename, channel_id, num_parts):
    logger.info('Preparing new upload for user %s...', user.id)
    channel = models.Channel.objects.get(id=channel_id, user=user)
    upload = models.Upload.objects.create(media_type='video', channel=channel)
    (
        upload.provider_upload_id,
        upload.presigned_upload_urls,
        upload.file.name,
    ) = _get_presigned_upload_url(
        upload=upload, filename=filename, num_parts=num_parts
    )
    upload.save(
        update_fields=('provider_upload_id', 'presigned_upload_urls', 'file')
    )
    title = _default_video_title_from_filename(filename)
    video = services.create_video(
        upload=upload, title=title, filename=filename
    )
    logger.info(
        'Done preparing upload for user %s, draft video %s', user.id, video.id
    )
    return upload, video


def _default_video_title_from_filename(filename):
    value = re.sub(r'[^\w\s-]', ' ', Path(filename).stem, re.IGNORECASE)
    value = re.sub(r'[-_]+', ' ', value)
    return re.sub(r' {2,}', ' ', value)


def _provider():
    return boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)


@async_task()
def complete(*, upload_id, parts):
    logger.info('Completing Upload...')
    upload = models.Upload.objects.get(id=upload_id)
    if upload.status == 'completed':
        logger.warning('Upload %s already completed, exiting...', upload.id)
        return None

    bucket_name = upload.file.field.storage.bucket_name
    object_name = upload.file.name
    provider_upload_id = upload.provider_upload_id
    if not provider_upload_id:
        logger.warning(
            'Upload %s provider_upload_id not set, exiting... '
            'Manually investigate.',
            upload.id,
        )
        return None

    # TODO: verify response
    _provider().complete_multipart_upload(
        Bucket=bucket_name,
        Key=object_name,
        MultipartUpload={
            'Parts': [
                {'ETag': p['etag'], 'PartNumber': p['part_number']}
                for p in parts
            ]
        },
        UploadId=provider_upload_id,
    )
    transcode_manager.create_transcodes(video_id=upload.video.id)
    _mark_upload_completed(upload)
    logger.info(
        'Completed Upload %s, transcoding started for video %s',
        upload.id,
        upload.video.id,
    )


def _mark_upload_completed(upload):
    upload.status = 'completed'
    upload.save(update_fields=('status',))
