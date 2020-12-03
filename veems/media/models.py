from django.db import models

from ..common.models import BaseModel
from .storage_backends import UploadStorage

TRANSCODE_JOB_CHOICES = (
    ('created', 'created'),
    ('processing', 'processing'),
    ('completed', 'completed'),
    ('failed', 'failed'),
)


def _upload_file_upload_to(instance, filename):
    return f'{instance.id}/{filename}'


class Upload(BaseModel):
    presigned_upload_url = models.URLField()
    media_type = models.CharField(max_length=200)
    file = models.FileField(
        upload_to=_upload_file_upload_to, storage=UploadStorage
    )

    @property
    def lease_id(self):
        return self.id


class TranscodeJob(BaseModel):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    profile = models.CharField(max_length=100)
    executor = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=TRANSCODE_JOB_CHOICES)
    started_on = models.DateTimeField(db_index=True, null=True)
    ended_on = models.DateTimeField(db_index=True, null=True)
    # TODO: failure context
