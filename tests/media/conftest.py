from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from veems.media import models

TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'
VIDEO_PATH_2160_30FPS = TEST_DATA_DIR / '2160p_30fps.mp4'


@pytest.fixture
def upload(upload_factory):
    return upload_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def video(video_factory):
    return video_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def upload_factory():
    def make(video_path):
        with video_path.open('rb') as file_:
            file_contents = file_.read()
        upload = models.Upload.objects.create(
            presigned_upload_url='htts://example.com/s3-blah',
            media_type='video',
            file=SimpleUploadedFile(video_path.name, file_contents)
        )
        return upload

    return make


@pytest.fixture
def video_factory(upload_factory):
    def make(video_path):
        upload = upload_factory(video_path=video_path)
        return models.Video.objects.create(upload=upload)

    return make
