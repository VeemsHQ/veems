from pathlib import Path

from django.utils import timezone
import pytest

from veems.media.video.transcoder.transcoder_executor import ffmpeg
from veems.media.models import TranscodeJob, Upload

pytestmark = pytest.mark.django_db
VIDEO_PATH = Path(__file__).parent.parent / 'test_data/1080p.mov'
INVALID_VIDEO_PATH = Path(__file__).parent.parent / 'test_data/not_a_video.mov'


def test_get_metadata():
    metadata = ffmpeg._get_metadata(video_path=VIDEO_PATH)

    assert metadata == {
        'width': 1920,
        'height': 1080,
    }


class TestTranscode:
    @pytest.fixture
    def transcode_job_factory(self):
        def make(profile):
            upload = Upload.objects.create(media_type='video/quicktime')
            return TranscodeJob.objects.create(
                upload=upload,
                profile=profile,
                executor='ffmpeg',
                status='created',
                started_on=timezone.now(),
            )

        return make

    @pytest.mark.parametrize(
        'transcode_profile_name, exp_width_height',
        [
            ('webm360p', (640, 360)),
            ('webm720p', (1280, 720)),
        ]
    )
    def test(
        self, transcode_job_factory, transcode_profile_name, exp_width_height
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=VIDEO_PATH
        )

        assert isinstance(result_path, Path)
        assert result_path.exists()
        metadata = ffmpeg._get_metadata(video_path=result_path)
        exp_width, exp_height = exp_width_height
        assert metadata == {
            'width': exp_width,
            'height': exp_height,
        }
        assert transcode_job.status == 'completed'
        assert transcode_job.ended_on

    def test_transcode_job_failed_when_video_file_is_not_valid(
        self, transcode_job
    ):
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=INVALID_VIDEO_PATH
        )

        assert result_path is None
        assert transcode_job.status == 'failed'
        assert transcode_job.ended_on
