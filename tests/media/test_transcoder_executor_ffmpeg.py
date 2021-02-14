from pathlib import Path
from unittest.mock import ANY
import shutil

import pytest
import m3u8

from veems.media.transcoder.transcoder_executor import ffmpeg
from veems.media import models, services
from veems.media.transcoder import transcoder_profiles
from tests import constants

pytestmark = pytest.mark.django_db
MODULE = 'veems.media.transcoder.transcoder_executor.ffmpeg'
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'


@pytest.mark.xfail
def test_create_segments_for_video(tmpdir, video_with_renditions_and_segments):
    video_path = constants.VIDEO_PATH_1080_30FPS_VERT
    profile = transcoder_profiles.Webm360p
    video, _ = video_with_renditions_and_segments
    video_rendition = video.renditions.first()
    video_rendition_id = video_rendition.id
    video_id = video_rendition.video_id

    (
        segments_playlist_file,
        segment_paths,
        codecs_string,
    ) = ffmpeg._create_segments_for_video(
        video_path=video_path,
        profile=profile,
        tmp_dir=tmpdir,
        video_rendition_id=video_rendition_id,
        video_id=video_id,
    )

    exp_num_segments = 13
    assert len(segment_paths) == exp_num_segments
    assert all(p.exists() and isinstance(p, Path) for p in segment_paths)
    assert isinstance(segments_playlist_file, Path)
    assert segments_playlist_file.exists()

    assert codecs_string == 'avc1.640028,mp4a.40.2'

    segment_names_durations = [
        (p.name, services.get_metadata(p)['summary']['duration'])
        for p in segment_paths
    ]
    exp_segment_names_durations = [
        ('0.ts', 9.2092),
        ('1.ts', 3.3033),
        ('2.ts', 4.337667),
        ('3.ts', 7.540867),
        ('4.ts', 4.537867),
        ('5.ts', 4.6046),
        ('6.ts', 6.006),
        ('7.ts', 8.341667),
        ('8.ts', 3.036367),
        ('9.ts', 6.773433),
        ('10.ts', 5.472133),
        ('11.ts', 8.341667),
        ('12.ts', 5.9059),
    ]
    assert segment_names_durations == exp_segment_names_durations
    exp_playlist = f"""
    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-TARGETDURATION:9
    #EXT-X-MEDIA-SEQUENCE:0
    #EXT-X-PLAYLIST-TYPE:VOD
    #EXTINF:9.209200,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/0.ts
    #EXTINF:3.303300,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/1.ts
    #EXTINF:4.337667,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/2.ts
    #EXTINF:7.540867,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/3.ts
    #EXTINF:4.537867,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/4.ts
    #EXTINF:4.604600,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/5.ts
    #EXTINF:6.006000,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/6.ts
    #EXTINF:8.341667,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/7.ts
    #EXTINF:3.036367,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/8.ts
    #EXTINF:6.773433,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/9.ts
    #EXTINF:5.472133,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/10.ts
    #EXTINF:8.341667,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/11.ts
    #EXTINF:5.905900,
    /videos/{video_id}/renditions/{video_rendition_id}/segments/12.ts
    #EXT-X-ENDLIST
    """
    assert (
        m3u8.load(str(segments_playlist_file)).dumps()
        == m3u8.loads(exp_playlist).dumps()
    )


@pytest.mark.parametrize(
    'video_path, exp_offsets',
    [
        (
            constants.VIDEO_PATH_2160_30FPS_10MIN,
            (
                15,
                46,
                77,
                108,
                139,
                171,
                202,
                233,
                264,
                295,
                326,
                357,
                388,
                419,
                450,
                481,
                513,
                544,
                575,
                606,
                637,
            ),
        ),
        (constants.VIDEO_PATH_2160_30FPS, (5,)),
        (constants.VID_1920_X_960, (5,)),
        (constants.VIDEO_PATH_1080_30FPS_VERT, (19, 57)),
    ],
)
def test_get_thumbnail_time_offsets(video_path, exp_offsets):
    time_offsets = ffmpeg._get_thumbnail_time_offsets(video_path=video_path)

    assert time_offsets == exp_offsets


class TestTranscode:
    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name, exp_metadata',
        [
            (
                constants.VID_720P_24FPS,
                'webm_144p',
                {
                    'audio_codec': None,
                    'duration': 5,
                    'framerate': 24,
                    'height': 144,
                    'video_codec': 'vp9',
                    'width': 256,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VID_1920_X_960,
                'webm_1080p',
                {
                    'audio_codec': 'opus',
                    'duration': 10,
                    'framerate': 30,
                    'height': 1080,
                    'video_codec': 'vp9',
                    'width': 2160,
                    'file_size': ANY,
                    'codecs_string': 'avc1.640032,mp4a.40.2',
                },
            ),
            (
                constants.VIDEO_PATH_1080_30FPS_VERT,
                'webm_240p',
                {
                    'audio_codec': 'opus',
                    'duration': 77,
                    'framerate': 30,
                    'height': 240,
                    'video_codec': 'vp9',
                    'width': 136,
                    'file_size': ANY,
                    'codecs_string': 'avc1.64000c,mp4a.40.2',
                },
            ),
            (
                constants.VIDEO_PATH_2160_30FPS,
                'webm_360p',
                {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VIDEO_PATH_2160_30FPS,
                'webm_720p',
                {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 720,
                    'video_codec': 'vp9',
                    'width': 1280,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VIDEO_PATH_2160_30FPS,
                'webm_1080p',
                {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 1080,
                    'video_codec': 'vp9',
                    'width': 1920,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VIDEO_PATH_2160_30FPS,
                'webm_1440p',
                {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 1440,
                    'video_codec': 'vp9',
                    'width': 2560,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VIDEO_PATH_2160_30FPS,
                'webm_2160p',
                {
                    'audio_codec': None,
                    'duration': 10,
                    'framerate': 30,
                    'height': 2160,
                    'video_codec': 'vp9',
                    'width': 3840,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VIDEO_PATH_1080_30FPS_VERT,
                'webm_360p',
                {
                    'audio_codec': 'opus',
                    'duration': 77,
                    'framerate': 30,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 202,
                    'file_size': ANY,
                    'codecs_string': 'avc1.64000d,mp4a.40.2',
                },
            ),
            (
                constants.VIDEO_PATH_1080_60FPS,
                'webm_360p_high',
                {
                    'audio_codec': 'opus',
                    'duration': 12,
                    'framerate': 60,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': ANY,
                    'codecs_string': 'avc1.64001f,mp4a.40.2',
                },
            ),
            (
                constants.VIDEO_PATH_2160_60FPS,
                'webm_360p_high',
                {
                    'audio_codec': 'opus',
                    'duration': 13,
                    'framerate': 60,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 640,
                    'file_size': ANY,
                    'codecs_string': 'avc1.64001f,mp4a.40.2',
                },
            ),
            (
                constants.VIDEO_PATH_2160_24FPS,
                'webm_360p',
                {
                    'audio_codec': None,
                    'duration': 37,
                    'framerate': 24,
                    'height': 360,
                    'video_codec': 'vp9',
                    'width': 682,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
            (
                constants.VID_1280_X_720,
                'webm_240p',
                {
                    'audio_codec': None,
                    'duration': 32.0,
                    'framerate': 25,
                    'height': 240,
                    'video_codec': 'vp9',
                    'width': 426,
                    'file_size': ANY,
                    'codecs_string': None,
                },
            ),
        ],
    )
    def test(
        self,
        transcode_job_factory,
        transcode_profile_name,
        source_file_path,
        exp_metadata,
        mocker,
    ):
        transcode_job = transcode_job_factory(profile=transcode_profile_name)
        video_rendition, thumbnails = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=source_file_path
        )

        # Check video transcoded & persisted
        assert isinstance(video_rendition, models.VideoRendition)
        assert video_rendition.file
        assert video_rendition.name == transcode_profile_name
        assert video_rendition.width == exp_metadata['width']
        assert video_rendition.height == exp_metadata['height']
        assert video_rendition.duration == exp_metadata['duration']
        assert video_rendition.framerate == exp_metadata['framerate']
        assert video_rendition.audio_codec == exp_metadata['audio_codec']
        assert video_rendition.video_codec == exp_metadata['video_codec']
        assert video_rendition.codecs_string == exp_metadata['codecs_string']
        assert video_rendition.ext == 'webm'
        assert video_rendition.container == 'webm'
        assert video_rendition.file_size == exp_metadata['file_size']
        assert video_rendition.metadata
        assert sorted(video_rendition.metadata.keys()) == sorted(
            ('summary', 'video_stream', 'audio_stream', 'format')
        )

        # Check video is also updated
        video = video_rendition.video
        assert video.duration == video_rendition.duration
        assert video.framerate == video_rendition.framerate
        assert video.is_viewable is True
        assert video.default_thumbnail_image

        assert thumbnails
        assert all(
            isinstance(t, models.VideoRenditionThumbnail) for t in thumbnails
        )
        # Check thumbnails created
        assert thumbnails
        for thumbnail_record in thumbnails:
            assert isinstance(thumbnail_record, models.VideoRenditionThumbnail)
            assert thumbnail_record.time_offset_secs > 0
            assert thumbnail_record.file
            assert thumbnail_record.file.name.endswith('.jpg')
            assert thumbnail_record.ext == 'jpg'
            assert thumbnail_record.width == exp_metadata['width']
            assert thumbnail_record.height == exp_metadata['height']

        assert transcode_job.status == 'completed'
        assert transcode_job.ended_on

        # Check Segments were created
        assert video_rendition.rendition_segments.count() > 0
        for segment in video_rendition.rendition_segments.all():
            assert segment.segment_number is not None
            assert segment.file

    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name',
        [
            (constants.VIDEO_PATH_360_60FPS, 'webm_720p'),
            (constants.VIDEO_PATH_360_60FPS, 'webm_1080p'),
            (constants.VIDEO_PATH_360_60FPS, 'webm_2160p'),
            (constants.VIDEO_PATH_1080_60FPS, 'webm_2160p'),
        ],
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
        assert not models.VideoRendition.objects.filter(
            video=transcode_job.video
        ).count()

    @pytest.mark.parametrize(
        'source_file_path, transcode_profile_name',
        [
            (constants.VIDEO_PATH_1080_60FPS, 'webm_720p'),
            (constants.VIDEO_PATH_2160_30FPS, 'webm_720p_high'),
        ],
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
        assert not models.VideoRendition.objects.filter(
            video=transcode_job.video
        ).count()

    def test_transcode_job_failed_when_ffmpeg_returns_an_error(
        self, transcode_job_factory, mocker
    ):
        mocker.patch(
            f'{MODULE}._ffmpeg_transcode_video',
            side_effect=[
                ffmpeg.TranscodeException('msg', stderr='command error output')
            ],
        )
        transcode_job = transcode_job_factory(profile='webm_240p')

        result_path = ffmpeg.transcode(
            transcode_job=transcode_job,
            source_file_path=constants.VIDEO_PATH_1080_30FPS_VERT,
        )

        assert result_path is None
        assert transcode_job.status == 'failed'
        assert transcode_job.ended_on
        assert transcode_job.failure_context == 'command error output'
        assert not models.VideoRendition.objects.filter(
            video=transcode_job.video
        ).count()

    def test_transcode_job_failed_when_video_file_is_not_valid(
        self, transcode_job
    ):
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job,
            source_file_path=constants.INVALID_VIDEO_PATH,
        )

        assert result_path is None
        assert transcode_job.status == 'failed'
        assert transcode_job.ended_on
        assert not models.VideoRendition.objects.filter(
            video=transcode_job.video
        ).count()

    def test_raises_if_source_file_path_does_not_exist(self, transcode_job):
        result_path = ffmpeg.transcode(
            transcode_job=transcode_job, source_file_path=Path('not_found')
        )

        assert result_path is None
        assert transcode_job.status == 'failed'
        assert transcode_job.ended_on
        assert transcode_job.failure_context is None
        assert not models.VideoRendition.objects.filter(
            video=transcode_job.video
        ).count()


def test_ffmpeg_generate_thumbnails(tmpdir):
    video_path = Path(tmpdir / constants.VID_1920_X_960.name)
    shutil.copyfile(constants.VID_1920_X_960, video_path)

    thumbnails = ffmpeg._ffmpeg_generate_thumbnails(
        video_file_path=video_path,
        profile=transcoder_profiles.Webm720p,
    )

    assert thumbnails
    for offset, thumb_path in thumbnails:
        assert offset > 0
        assert thumb_path.exists()
        metadata = services.get_metadata(thumb_path)
        # Height is fixed and width is auto.
        assert metadata['summary']['height'] == 720
        assert metadata['summary']['width'] == 1440
