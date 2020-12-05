import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3

from veems.media import models

pytestmark = pytest.mark.django_db


def test_upload_file_upload_to(upload):
    result = models._upload_file_upload_to(
        instance=upload, filename='blah.mp4'
    )

    assert result == f'{upload.id}.mp4'


def test_mediaformat_upload_to(video, simple_uploaded_file):
    mediaformat = models.MediaFormat.objects.create(
        video=video,
        file=simple_uploaded_file,
        name='360p',
        ext='webm',
        filesize=1,
    )

    result = models._mediaformat_upload_to(
        instance=mediaformat, filename='360p.webm'
    )

    assert result == f'{mediaformat.id}.webm'


class TestUpload:
    def test_set_file_using_uploaded_file(self):
        upload = models.Upload.objects.create(
            presigned_upload_url='https://example.com', media_type='video'
        )
        file_ = SimpleUploadedFile(
            'video.mp4',
            b'data',
        )

        upload.file = file_
        upload.save()
        upload.refresh_from_db()

        assert upload.file.name == f'{upload.id}.mp4'
        assert upload.file.url.startswith(
            f'http://localhost:4566/veems-local-uploaded/{upload.id}.mp4'
            '?AWSAccessKeyId'
        )

    def test_file_uploaded_outside_the_applocation(self, settings):
        # This tests the flow where the file is uploaded to the storage
        # bucket completely outside of the application itself
        # (on the client side using pre-signed-url upload process
        upload = models.Upload.objects.create(
            presigned_upload_url='https://example.com', media_type='video'
        )

        uploaded_filename = f'{upload.id}/video.mp4'

        # Upload the file completely outside of Django
        s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
        s3.upload_fileobj(
            io.BytesIO(b'data'), models.UploadStorage.bucket_name,
            uploaded_filename
        )

        # Set the Django file field to point to that file path
        upload.file.name = uploaded_filename
        upload.save()

        # Check file can be accessed as if it was uploaded within Django
        upload.refresh_from_db()
        assert upload.file.name == uploaded_filename
        assert upload.file.url.startswith(
            f'http://localhost:4566/veems-local-uploaded/{upload.id}/'
            f'video.mp4?AWSAccessKeyId'
        )
