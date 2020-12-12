from unittest.mock import ANY

import pytest

from veems.media import services
from tests import constants

pytestmark = pytest.mark.django_db


def test_mark_transcode_job_completed(transcode_job_factory):
    job = transcode_job_factory(profile='240p')

    updated_job = services.mark_transcode_job_completed(transcode_job=job)

    assert updated_job.status == 'completed'
    assert updated_job.id == job.id


def test_mark_transcode_job_failed(transcode_job_factory):
    job = transcode_job_factory(profile='240p')

    updated_job = services.mark_transcode_job_failed(transcode_job=job)

    assert updated_job.status == 'failed'
    assert updated_job.id == job.id


@pytest.mark.parametrize(
    'video_path, exp_metadata', [
        (
            constants.VIDEO_PATH_2160_30FPS, {
                'width': 3840,
                'height': 2160,
                'framerate': 30,
                'duration': 10.1,
                'video_codec': 'h264',
                'audio_codec': None,
                'file_size': ANY,
                'video_aspect_ratio': '16:9',
            }
        ),
        (
            constants.VIDEO_PATH_1080_30FPS_VERT,
            {
                'duration': 77,
                'framerate': 30,
                'height': 1920,
                'width': 1080,
                'video_codec': 'vp9',
                'audio_codec': 'opus',
                'file_size': ANY,
                'video_aspect_ratio': '9:16',
            },
        ),
    ]
)
def test_get_metadata(video_path, exp_metadata):
    metadata = services.get_metadata(video_path=video_path)

    assert metadata == exp_metadata
