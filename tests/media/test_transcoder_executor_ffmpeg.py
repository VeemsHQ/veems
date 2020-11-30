from pathlib import Path

from django.utils import timezone
import pytest

from veems.media.video.transcoder.transcoder_executor import ffmpeg
from veems.media.models import TranscodeJob, Upload

pytestmark = pytest.mark.django_db
VIDEO_PATH = Path(__file__).parent.parent / 'test_data/2160p_30fps.mp4'
INVALID_VIDEO_PATH = Path(__file__).parent.parent / 'test_data/not_a_video.mov'


def test_get_metadata():
    metadata = ffmpeg._get_metadata(video_path=VIDEO_PATH)

    assert metadata == {
        'width': 1920,
        'height': 1080,
        'framerate': 30,
    }


class TestTranscode:
    @pytest.fixture
    def transcode_job_factory(self):
        def make(profile):
            upload = Upload.objects.create(media_type='video/mp4')
            return TranscodeJob.objects.create(
                upload=upload,
                profile=profile,
                executor='ffmpeg',
                status='created',
                started_on=timezone.now(),
            )

        return make

    @pytest.mark.parametrize(
        'transcode_profile_name, exp_width_height', [
            # ('webm_360p', (640, 360)),
            # ('webm_720p', (1280, 720)),
            ('webm_1080p', (1920, 1080)),
            ('webm_2160p', (3840, 2160)),
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
        import ipdb; ipdb.set_trace()
        assert result_path.exists()
        metadata = ffmpeg._get_metadata(video_path=result_path)
        exp_width, exp_height = exp_width_height
        assert metadata == {
            'width': exp_width,
            'height': exp_height,
            'framerate': 30,
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
