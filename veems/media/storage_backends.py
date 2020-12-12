from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class UploadStorage(S3Boto3Storage):
    bucket_name = settings.BUCKET_UPLOADS


class MediaFileStorage(S3Boto3Storage):
    bucket_name = settings.BUCKET_MEDIA_FILES


class MediaFileThumbnailStorage(S3Boto3Storage):
    bucket_name = settings.BUCKET_MEDIA_FILE_THUMBNAILS
