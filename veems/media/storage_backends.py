from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.BUCKET_MEDIA
    custom_domain = settings.BUCKET_MEDIA_CUSTOM_DOMAIN
    default_acl = settings.BUCKET_MEDIA_DEFAULT_ACL
