from pathlib import Path

import pytest

from veems.media.video.transcoder.transcoder_executor import ffmpeg

pytestmark = pytest.mark.django_db
VIDEO_PATH_2160_30FPS = (
    Path(__file__).parent.parent / 'test_data/2160p_30fps.mp4'
)
VIDEO_PATH_2160_24FPS = (
    Path(__file__).parent.parent / 'test_data/2160p_24fps.mp4'
)
VIDEO_PATH_2160_60FPS = (
    Path(__file__).parent.parent / 'test_data/2160p_60fps.mkv'
)
VIDEO_PATH_1080_60FPS = (
    Path(__file__).parent.parent / 'test_data/1080p_60fps.mp4'
)
VIDEO_PATH_1080_30FPS_VERT = (
    Path(__file__).parent.parent / 'test_data/1080p_30fps_vertical.webm'
)
VIDEO_PATH_360_60FPS = (
    Path(__file__).parent.parent / 'test_data/360p_60fps.webm'
)
INVALID_VIDEO_PATH = Path(__file__).parent.parent / 'test_data/not_a_video.mov'


def test_get_metadata():
    metadata = ffmpeg._get_metadata(video_path=VIDEO_PATH_2160_30FPS)

    assert metadata == {
        'width': 3840,
        'height': 2160,
        'framerate': 30,
    }


class TestTranscode:
    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name, exp_width_height, exp_fps',
        [
            (VIDEO_PATH_2160_30FPS, 'webm_360p', (640, 360), 30),
            (VIDEO_PATH_2160_30FPS, 'webm_720p', (1280, 720), 30),
            (VIDEO_PATH_2160_30FPS, 'webm_1080p', (1920, 1080), 30),
            (VIDEO_PATH_2160_30FPS, 'webm_2160p', (3840, 2160), 30),
            (VIDEO_PATH_1080_30FPS_VERT, 'webm_360p', (640, 360), 30),
            (VIDEO_PATH_1080_60FPS, 'webm_360p_high', (640, 360), 60),
            (VIDEO_PATH_2160_60FPS, 'webm_360p_high', (640, 360), 60),
            (VIDEO_PATH_2160_24FPS, 'webm_360p', (640, 360), 24),
        ]
    )
    def test(
        self, transcode_job_factory, transcode_profile_name, exp_width_height,
        source_file_path, exp_fps
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=source_file_path
        )

        assert isinstance(result_path, Path)
        assert result_path.exists()
        metadata = ffmpeg._get_metadata(video_path=result_path)
        exp_width, exp_height = exp_width_height
        assert metadata == {
            'width': exp_width,
            'height': exp_height,
            'framerate': exp_fps,
        }
        # TODO: check audio
        assert transcode_job.status == 'completed'
        assert transcode_job.ended_on

    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name', [
            (VIDEO_PATH_360_60FPS, 'webm_720p'),
            (VIDEO_PATH_360_60FPS, 'webm_1080p'),
            (VIDEO_PATH_360_60FPS, 'webm_2160p'),
            (VIDEO_PATH_1080_60FPS, 'webm_2160p'),
        ]
    )
    def test_cannot_transcode_into_resolution_higher_than_source_file(
        self, source_file_path, transcode_profile_name, transcode_job_factory
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=source_file_path
        )

        assert result_path is None
        assert transcode_job.status == 'completed'
        assert transcode_job.ended_on

    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name', [
            (VIDEO_PATH_1080_60FPS, 'webm_720p'),
            (VIDEO_PATH_2160_30FPS, 'webm_720p_high'),
        ]
    )
    def test_cannot_transcode_into_different_framerate(
        self, source_file_path, transcode_profile_name, transcode_job_factory
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=source_file_path
        )

        assert result_path is None
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
