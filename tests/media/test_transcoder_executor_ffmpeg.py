from pathlib import Path

import pytest

from veems.media.video.transcoder.transcoder_executor import ffmpeg
from veems.media import models

pytestmark = pytest.mark.django_db
VIDEO_PATH_2160_30FPS = (
    Path(__file__).parent.parent / 'test_data/2160p_30fps.mp4'
)
VIDEO_PATH_2160_30FPS_10MIN = (
    Path(__file__).parent.parent / 'test_data/360p_30fps_10min.mp4'
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


@pytest.mark.parametrize(
    'video_path, exp_metadata', [
        (
            VIDEO_PATH_2160_30FPS, {
                'width': 3840,
                'height': 2160,
                'framerate': 30,
                'duration': 10.1,
                'video_codec': 'h264',
                'audio_codec': None,
                'file_size': 54623999,
            }
        ),
        (
            VIDEO_PATH_1080_30FPS_VERT,
            {
                'duration': 77,
                'framerate': 30,
                'height': 1920,
                'width': 1080,
                'video_codec': 'vp9',
                'audio_codec': 'opus',
                'file_size': 26813061,
            },
        )
    ]
)
def test_get_metadata(video_path, exp_metadata):
    metadata = ffmpeg._get_metadata(video_path=video_path)

    assert metadata == exp_metadata


@pytest.mark.parametrize(
    'video_path, exp_offsets', [
        (
            VIDEO_PATH_2160_30FPS_10MIN, (
                15, 46, 77, 108, 139, 171, 202, 233, 264, 295, 326, 357, 388,
                419, 450, 481, 513, 544, 575, 606, 637
            )
        ), (VIDEO_PATH_2160_30FPS, (5, )),
        (VIDEO_PATH_1080_30FPS_VERT, (19, 57))
    ]
)
def test_get_thumbnail_time_offsets(video_path, exp_offsets):
    time_offsets = ffmpeg._get_thumbnail_time_offsets(video_path=video_path)

    assert time_offsets == exp_offsets


class TestTranscode:
    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name, exp_metadata', [
            (
                VIDEO_PATH_2160_30FPS, 'webm_360p', {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': 275477,
                }
            ),
            (
                VIDEO_PATH_2160_30FPS, 'webm_720p', {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 720,
                    'video_codec': 'vp9',
                    'width': 1280,
                    'file_size': 1106071,
                }
            ),
            (
                VIDEO_PATH_2160_30FPS, 'webm_1080p', {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 1080,
                    'video_codec': 'vp9',
                    'width': 1920,
                    'file_size': 2666458,
                }
            ),
            (
                VIDEO_PATH_2160_30FPS, 'webm_2160p', {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 2160,
                    'video_codec': 'vp9',
                    'width': 3840,
                    'file_size': 17327709,
                }
            ),
            (
                VIDEO_PATH_1080_30FPS_VERT, 'webm_360p', {
                    'audio_codec': 'opus',
                    'duration': 77,
                    'framerate': 30,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': 3693226,
                }
            ),
            (
                VIDEO_PATH_1080_60FPS, 'webm_360p_high', {
                    'audio_codec': 'opus',
                    'duration': 12,
                    'framerate': 60,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': 2490631,
                }
            ),
            (
                VIDEO_PATH_2160_60FPS, 'webm_360p_high', {
                    'audio_codec': 'opus',
                    'duration': 13,
                    'framerate': 60,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': 2338906,
                }
            ),
            (
                VIDEO_PATH_2160_24FPS, 'webm_360p', {
                    'audio_codec': None,
                    'duration': 37,
                    'framerate': 24,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': 1137905,
                }
            ),
        ]
    )
    def test(
        self, transcode_job_factory, transcode_profile_name, source_file_path,
        exp_metadata, mocker
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        result_path, thumbnails = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=source_file_path
        )

        # Check video transcoded
        assert isinstance(result_path, Path)
        assert result_path.exists()
        metadata = ffmpeg._get_metadata(video_path=result_path)
        assert metadata == exp_metadata
        # TODO: check audio
        # Check video persisted
        media_file = models.MediaFile.objects.get(video=transcode_job.video)
        assert media_file.file
        assert media_file.name == transcode_profile_name
        assert media_file.width == exp_metadata['width']
        assert media_file.height == exp_metadata['height']
        assert media_file.duration == metadata['duration']
        assert media_file.framerate == metadata['framerate']
        assert media_file.audio_codec == metadata['audio_codec']
        assert media_file.video_codec == metadata['video_codec']
        assert media_file.ext == 'webm'
        assert media_file.file_size == metadata['file_size']

        # Check thumbnails created
        assert thumbnails
        for time_offset, thumb_path in thumbnails:
            assert isinstance(time_offset, int)
            assert thumb_path.name.endswith('.jpg')
            thumb_meta = ffmpeg._get_metadata(thumb_path)
            assert thumb_meta['width'] == exp_metadata['width']
            assert thumb_meta['height'] == exp_metadata['height']
        # Check thumbnails persisted
        thumbnail_db_records = models.MediaFileThumbnail.objects.filter(
            media_file__video=transcode_job.video
        )
        assert len(thumbnail_db_records) == len(thumbnails)
        assert all(t.file for t in thumbnail_db_records)

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
        assert not models.MediaFile.objects.filter(video=transcode_job.video
                                                   ).count()

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
        assert not models.MediaFile.objects.filter(video=transcode_job.video
                                                   ).count()

    def test_transcode_job_failed_when_video_file_is_not_valid(
        self, transcode_job
    ):
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=INVALID_VIDEO_PATH
        )

        assert result_path is None
        assert transcode_job.status == 'failed'
        assert transcode_job.ended_on
        assert not models.MediaFile.objects.filter(video=transcode_job.video
                                                   ).count()

    def test_raises_if_source_file_path_does_not_exist(self, transcode_job):
        with pytest.raises(OSError):
            ffmpeg.transcode(
                transcode_job=transcode_job,
                source_file_path=Path('not_found')
            )

        assert not models.MediaFile.objects.filter(video=transcode_job.video
                                                   ).count()
