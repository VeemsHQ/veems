from django.conf import settings
import boto3

from . import models
from .transcoder import manager as transcode_manager

ONE_DAY_IN_SECS = 86400


def _get_presigned_upload_url(*, upload, filename):
    s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
    bucket_name = upload.file.field.storage.bucket_name
    object_name = models._upload_file_upload_to(
        instance=upload, filename=filename
    )
    response = s3.generate_presigned_url(
        'get_object',
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


def complete(upload_id):
    video_id = models.Video.objects.get(upload_id=upload_id).id
    transcode_manager.create_transcodes(video_id=video_id)
