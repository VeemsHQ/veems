from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
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
def simple_uploaded_file():
    with VIDEO_PATH_2160_30FPS.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(VIDEO_PATH_2160_30FPS.name, file_contents)


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
    def make(video_path, **kwargs):
        upload = upload_factory(video_path=video_path)
        return models.Video.objects.create(upload=upload, **kwargs)

    return make


@pytest.fixture
def transcode_job_factory(video):
    def make(profile, status='created', video_record=None):
        return models.TranscodeJob.objects.create(
            video=video_record or video,
            profile=profile,
            executor='ffmpeg',
            status=status,
            started_on=timezone.now(),
        )

    return make


@pytest.fixture
def transcode_job(transcode_job_factory):
    return transcode_job_factory(profile='webm_360p')
