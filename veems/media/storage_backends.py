from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class UploadStorage(S3Boto3Storage):
    bucket_name = settings.UPLOADED_OBJECT_STORAGE_BUCKET


class MediaFormatStorage(S3Boto3Storage):
    bucket_name = settings.MEDIA_FORMAT_OBJECT_STORAGE_BUCKET
