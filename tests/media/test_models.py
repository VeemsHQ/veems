import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3

from veems.media import models

pytestmark = pytest.mark.django_db


@pytest.fixture
def media_file(video, simple_uploaded_file):
    return models.MediaFile.objects.create(
        video=video,
        file=simple_uploaded_file,
        name='360p',
        ext='webm',
        file_size=1,
    )


def test_transcode_job(transcode_job):
    assert str(transcode_job
               ) == (f'<TranscodeJob {transcode_job.id} webm_360p created>')


def test_upload_file_upload_to(upload):
    result = models._upload_file_upload_to(
        instance=upload, filename='blah.mp4'
    )

    assert result == f'uploads/{upload.id}.mp4'


def test_media_file_upload_to(media_file):
    result = models._media_file_upload_to(
        instance=media_file, filename='360p.webm'
    )

    assert result == f'media_files/{media_file.id}.webm'


def test_media_file_thumbnail_upload_to(media_file):
    media_file_thumbnail = models.MediaFileThumbnail.objects.create(
        media_file=media_file, time_offset_secs=1
    )

    result = models._media_file_thumbnail_upload_to(
        instance=media_file_thumbnail, filename='something.jpg'
    )

    assert result == (
        f'media_files/thumbnails/{media_file.id}/{media_file_thumbnail.id}.jpg'
    )


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

        assert upload.file.name == f'uploads/{upload.id}.mp4'
        assert upload.file.url.startswith('http')
        assert 'AccessKeyId' in upload.file.url

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
            io.BytesIO(b'data'), models.STORAGE_BACKEND.bucket_name,
            uploaded_filename
        )

        # Set the Django file field to point to that file path
        upload.file.name = uploaded_filename
        upload.save()

        # Check file can be accessed as if it was uploaded within Django
        upload.refresh_from_db()
        assert upload.file.name == uploaded_filename
        assert upload.file.url.startswith('http')
        assert 'AccessKeyId' in upload.file.url, upload.file.url
        assert upload.id in upload.file.url
