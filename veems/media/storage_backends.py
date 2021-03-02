from django.conf import settings

from ..common.storage_backends import CustomS3Boto3Storage


class MediaStorage(CustomS3Boto3Storage):
    bucket_name = settings.BUCKET_MEDIA
    custom_domain = settings.BUCKET_MEDIA_CUSTOM_DOMAIN
    default_acl = settings.BUCKET_MEDIA_DEFAULT_ACL


class MediaStoragePublic(MediaStorage):
    default_acl = 'public-read'
