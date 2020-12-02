from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.utils import timezone
from ffprobe import FFProbe

from veems.media import models
from veems.media.video.transcoder import manager
from veems.media.video.transcoder import transcoder_profiles

pytestmark = pytest.mark.django_db

MODULE = 'veems.media.video.transcoder.manager'
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'
VIDEO_PATH = TEST_DATA_DIR / '2160p_30fps.mp4'


@pytest.fixture
def upload():
    with VIDEO_PATH.open('rb') as file_:
        file_contents = file_.read()
    return models.Upload.objects.create(
        presigned_upload_url='htts://example.com/s3-blah',
        media_type='video',
        file=SimpleUploadedFile(VIDEO_PATH.name, file_contents)
    )


@pytest.mark.parametrize(
    'video_filename, profile_cls, exp_result', [
        ('2160p_30fps.mp4', transcoder_profiles.WebM360p, True),
        ('2160p_30fps.mp4', transcoder_profiles.WebM720p, True),
        ('2160p_30fps.mp4', transcoder_profiles.WebM1080p, True),
        ('2160p_30fps.mp4', transcoder_profiles.WebM2160p, True),
        ('2160p_30fps.mp4', transcoder_profiles.WebM720pHigh, False),
        ('2160p_30fps.mp4', transcoder_profiles.WebM1080pHigh, False),
        ('2160p_30fps.mp4', transcoder_profiles.WebM2160pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.WebM360pHigh, True),
        ('360p_60fps.webm', transcoder_profiles.WebM360p, False),
        ('360p_60fps.webm', transcoder_profiles.WebM720p, False),
        ('360p_60fps.webm', transcoder_profiles.WebM720pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.WebM1080p, False),
        ('360p_60fps.webm', transcoder_profiles.WebM1080pHigh, False),
        ('360p_60fps.webm', transcoder_profiles.WebM2160p, False),
        ('360p_60fps.webm', transcoder_profiles.WebM2160pHigh, False),
        ('1080p_60fps.mp4', transcoder_profiles.WebM360pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.WebM720pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.WebM1080pHigh, True),
        ('1080p_60fps.mp4', transcoder_profiles.WebM2160pHigh, False),
        ('1080p_60fps.mp4', transcoder_profiles.WebM360p, False),
        ('1080p_60fps.mp4', transcoder_profiles.WebM720p, False),
        ('1080p_60fps.mp4', transcoder_profiles.WebM1080p, False),
        ('1080p_60fps.mp4', transcoder_profiles.WebM2160p, False),
    ]
)
def test_transcode_profile_does_apply(video_filename, profile_cls, exp_result):
    video_path = TEST_DATA_DIR / video_filename
    metadata = FFProbe(str(video_path))
    ffprobe_stream = metadata.video[0]

    result = manager._transcode_profile_does_apply(
        profile_cls=profile_cls, ffprobe_stream=ffprobe_stream
    )

    assert result == exp_result


class TestHandleUploadComplete:
    def test_creates_transcode_jobs(self, upload, mocker):
        mock_task_transcode = mocker.patch(f'{MODULE}.task_transcode')

        manager.handle_upload_complete(upload_id=upload.id)

        exp_num_jobs = len(transcoder_profiles.PROFILES)

        assert models.TranscodeJob.objects.count() == exp_num_jobs
        assert (
            models.TranscodeJob.objects.filter(status='created'
                                               ).count() == exp_num_jobs
        )
        assert mock_task_transcode.delay.call_count == exp_num_jobs


def test_task_transcode(upload, mocker):
    mock_executor = mocker.patch(f'{MODULE}.transcode_executor')
    transcode_job = models.TranscodeJob.objects.create(
        upload=upload,
        profile='webm_360p',
        executor='ffmpeg',
        status='created',
        started_on=timezone.now(),
    )

    manager.task_transcode(
        upload_id=upload.id, transcode_job_id=transcode_job.id
    )

    mock_executor.transcode.assert_called_once_with(
        transcode_job=transcode_job,
        source_file_path=mocker.ANY,
    )
    transcode_job.refresh_from_db()
    assert transcode_job.status == 'processing'
    assert transcode_job.started_on
    # Check that the file sent to the transcode job
    # is the uploaded file.
    source_file_path = (
        mock_executor.transcode.call_args.kwargs['source_file_path']
    )
    with source_file_path.open('rb') as file_:
        file_data = file_.read()
    assert file_data == upload.file.read()
