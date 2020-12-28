import pytest
from pytest_voluptuous import S
import m3u8

from veems.media import services, models
from veems.media.transcoder.transcoder_executor import ffmpeg
from veems.media.transcoder import transcoder_profiles
from tests import constants

pytestmark = pytest.mark.django_db


def test_mark_transcode_job_completed(transcode_job_factory):
    job = transcode_job_factory(profile='240p')

    updated_job = services.mark_transcode_job_completed(transcode_job=job)

    assert updated_job.status == 'completed'
    assert updated_job.ended_on
    assert updated_job.id == job.id


def test_mark_transcode_job_failed(transcode_job_factory):
    job = transcode_job_factory(profile='240p')

    updated_job = services.mark_transcode_job_failed(transcode_job=job)

    assert updated_job.status == 'failed'
    assert updated_job.ended_on
    assert updated_job.id == job.id


def test_mark_transcode_job_processing(transcode_job_factory):
    job = transcode_job_factory(profile='240p')

    updated_job = services.mark_transcode_job_processing(transcode_job=job)

    assert updated_job.status == 'processing'
    assert updated_job.started_on
    assert updated_job.id == job.id


@pytest.mark.parametrize(
    'video_path, exp_metadata',
    [
        (
            constants.VIDEO_PATH_2160_30FPS,
            S(
                {
                    'audio_stream': None,
                    'format': {
                        'bit_rate': '43266533',
                        'duration': '10.100000',
                        'filename': str(constants.VIDEO_PATH_2160_30FPS),
                        'format_long_name': 'QuickTime / MOV',
                        'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
                        'nb_programs': 0,
                        'nb_streams': 1,
                        'probe_score': 100,
                        'size': '54623999',
                        'start_time': '0.000000',
                        'tags': {
                            'compatible_brands': 'mp42mp41',
                            'creation_time': '2018-07-10T20:22:55.000000Z',
                            'major_brand': 'mp42',
                            'minor_version': '0',
                        },
                    },
                    'summary': {
                        'audio_codec': None,
                        'duration': 10.1,
                        'file_size': 54623999,
                        'framerate': 30,
                        'height': 2160,
                        'video_aspect_ratio': '16:9',
                        'video_bit_rate': 43266533,
                        'video_codec': 'h264',
                        'width': 3840,
                    },
                    'video_stream': {
                        'avg_frame_rate': '30/1',
                        'bit_rate': '43255196',
                        'bits_per_raw_sample': '8',
                        'chroma_location': 'left',
                        'closed_captions': 0,
                        'codec_long_name': (
                            'H.264 / AVC / MPEG-4 AVC / MPEG-4 part ' '10'
                        ),
                        'codec_name': 'h264',
                        'codec_tag': '0x31637661',
                        'codec_tag_string': 'avc1',
                        'codec_time_base': '1/60',
                        'codec_type': 'video',
                        'coded_height': 2160,
                        'coded_width': 3840,
                        'color_primaries': 'bt709',
                        'color_range': 'tv',
                        'color_space': 'bt709',
                        'color_transfer': 'bt709',
                        'display_aspect_ratio': '16:9',
                        'disposition': {
                            'attached_pic': 0,
                            'clean_effects': 0,
                            'comment': 0,
                            'default': 1,
                            'dub': 0,
                            'forced': 0,
                            'hearing_impaired': 0,
                            'karaoke': 0,
                            'lyrics': 0,
                            'original': 0,
                            'timed_thumbnails': 0,
                            'visual_impaired': 0,
                        },
                        'duration': '10.100000',
                        'duration_ts': 303000,
                        'has_b_frames': 1,
                        'height': 2160,
                        'index': 0,
                        'is_avc': 'true',
                        'level': 52,
                        'nal_length_size': '4',
                        'nb_frames': '303',
                        'pix_fmt': 'yuv420p',
                        'profile': 'High',
                        'r_frame_rate': '30/1',
                        'refs': 1,
                        'sample_aspect_ratio': '1:1',
                        'start_pts': 0,
                        'start_time': '0.000000',
                        'tags': {
                            'creation_time': '2018-07-10T20:22:55.000000Z',
                            'encoder': 'AVC Coding',
                            'handler_name': str,
                            'language': 'eng',
                        },
                        'time_base': '1/30000',
                        'width': 3840,
                    },
                },
                required=False,
            ),
        ),
        (
            constants.VIDEO_PATH_1080_30FPS_VERT,
            S(
                {
                    'audio_stream': {
                        'avg_frame_rate': '0/0',
                        'bits_per_sample': 0,
                        'channel_layout': 'stereo',
                        'channels': 2,
                        'codec_long_name': (
                            'Opus (Opus Interactive Audio Codec)'
                        ),
                        'codec_name': 'opus',
                        'codec_tag': '0x0000',
                        'codec_tag_string': '[0][0][0][0]',
                        'codec_time_base': '1/48000',
                        'codec_type': 'audio',
                        'disposition': {
                            'attached_pic': 0,
                            'clean_effects': 0,
                            'comment': 0,
                            'default': 1,
                            'dub': 0,
                            'forced': 0,
                            'hearing_impaired': 0,
                            'karaoke': 0,
                            'lyrics': 0,
                            'original': 0,
                            'timed_thumbnails': 0,
                            'visual_impaired': 0,
                        },
                        'index': 1,
                        'r_frame_rate': '0/0',
                        'sample_fmt': 'fltp',
                        'sample_rate': '48000',
                        'start_pts': -7,
                        'start_time': '-0.007000',
                        'tags': {
                            'DURATION': '00:01:17.441000000',
                            'language': 'eng',
                        },
                        'time_base': '1/1000',
                    },
                    'format': {
                        'bit_rate': '2769908',
                        'duration': '77.441000',
                        'filename': str(constants.VIDEO_PATH_1080_30FPS_VERT),
                        'format_long_name': 'Matroska / WebM',
                        'format_name': 'matroska,webm',
                        'nb_programs': 0,
                        'nb_streams': 2,
                        'probe_score': 100,
                        'size': '26813061',
                        'start_time': '-0.007000',
                        'tags': {'ENCODER': 'Lavf58.45.100'},
                    },
                    'summary': {
                        'audio_codec': 'opus',
                        'duration': 77.0,
                        'file_size': 26813061,
                        'framerate': 30,
                        'height': 1920,
                        'video_aspect_ratio': '9:16',
                        'video_bit_rate': 2769908,
                        'video_codec': 'vp9',
                        'width': 1080,
                    },
                    'video_stream': {
                        'avg_frame_rate': '30000/1001',
                        'closed_captions': 0,
                        'codec_long_name': 'Google VP9',
                        'codec_name': 'vp9',
                        'codec_tag': '0x0000',
                        'codec_tag_string': '[0][0][0][0]',
                        'codec_time_base': '1001/30000',
                        'codec_type': 'video',
                        'coded_height': 1920,
                        'coded_width': 1080,
                        'color_primaries': 'bt709',
                        'color_range': 'tv',
                        'color_space': 'bt709',
                        'color_transfer': 'bt709',
                        'display_aspect_ratio': '9:16',
                        'disposition': {
                            'attached_pic': 0,
                            'clean_effects': 0,
                            'comment': 0,
                            'default': 1,
                            'dub': 0,
                            'forced': 0,
                            'hearing_impaired': 0,
                            'karaoke': 0,
                            'lyrics': 0,
                            'original': 0,
                            'timed_thumbnails': 0,
                            'visual_impaired': 0,
                        },
                        'has_b_frames': 0,
                        'height': 1920,
                        'index': 0,
                        'level': -99,
                        'pix_fmt': 'yuv420p',
                        'profile': 'Profile 0',
                        'r_frame_rate': '30000/1001',
                        'refs': 1,
                        'sample_aspect_ratio': '1:1',
                        'start_pts': 0,
                        'start_time': '0.000000',
                        'tags': {
                            'DURATION': '00:01:17.410000000',
                            'language': 'eng',
                        },
                        'time_base': '1/1000',
                        'width': 1080,
                    },
                },
                required=False,
            ),
        ),
        (
            constants.VID_4k_2,
            S(
                {
                    'audio_stream': None,
                    'format': {
                        'bit_rate': '12216038',
                        'duration': '30.233000',
                        'filename': str(constants.VID_4k_2),
                        'format_long_name': 'Matroska / WebM',
                        'format_name': 'matroska,webm',
                        'nb_programs': 0,
                        'nb_streams': 1,
                        'probe_score': 100,
                        'size': '46165938',
                        'start_time': '0.000000',
                        'tags': {'encoder': 'google/video-file'},
                    },
                    'summary': {
                        'audio_codec': None,
                        'duration': 30.233,
                        'file_size': 46165938,
                        'framerate': 30,
                        'height': 2160,
                        'video_aspect_ratio': '16:9',
                        'video_bit_rate': 12216038,
                        'video_codec': 'vp9',
                        'width': 3840,
                    },
                    'video_stream': {
                        'avg_frame_rate': '30/1',
                        'closed_captions': 0,
                        'codec_long_name': 'Google VP9',
                        'codec_name': 'vp9',
                        'codec_tag': '0x0000',
                        'codec_tag_string': '[0][0][0][0]',
                        'codec_time_base': '1/30',
                        'codec_type': 'video',
                        'coded_height': 2160,
                        'coded_width': 3840,
                        'color_primaries': 'bt709',
                        'color_range': 'tv',
                        'color_space': 'bt709',
                        'color_transfer': 'bt709',
                        'display_aspect_ratio': '16:9',
                        'disposition': {
                            'attached_pic': 0,
                            'clean_effects': 0,
                            'comment': 0,
                            'default': 1,
                            'dub': 0,
                            'forced': 0,
                            'hearing_impaired': 0,
                            'karaoke': 0,
                            'lyrics': 0,
                            'original': 0,
                            'timed_thumbnails': 0,
                            'visual_impaired': 0,
                        },
                        'has_b_frames': 0,
                        'height': 2160,
                        'index': 0,
                        'level': -99,
                        'pix_fmt': 'yuv420p',
                        'profile': 'Profile 0',
                        'r_frame_rate': '30/1',
                        'refs': 1,
                        'sample_aspect_ratio': '1:1',
                        'start_pts': 0,
                        'start_time': '0.000000',
                        'tags': {'language': 'eng'},
                        'time_base': '1/1000',
                        'width': 3840,
                    },
                },
                required=False,
            ),
        ),
    ],
)
def test_get_metadata(video_path, exp_metadata):
    metadata = services.get_metadata(video_path=video_path)

    assert metadata == exp_metadata
    assert sorted(metadata.keys()) == sorted(
        ('audio_stream', 'video_stream', 'summary', 'format')
    )


def test_persist_video_rendition_segments(video, simple_uploaded_file, tmpdir):
    video_rendition = models.VideoRendition.objects.create(
        video=video,
        file=simple_uploaded_file,
        name='360p',
        ext='webm',
        file_size=1,
    )
    assert not video_rendition.playlist_file
    video_path = constants.VIDEO_PATH_1080_30FPS_VERT
    profile = transcoder_profiles.Webm360p

    (
        segments_playlist_file,
        segment_paths,
        _,
    ) = ffmpeg._create_segments_for_video(
        video_path=video_path,
        profile=profile,
        tmp_dir=tmpdir,
        video_rendition_id=video_rendition.id,
        video_id=video_rendition.video_id,
    )

    services.persist_video_rendition_segments(
        video_rendition=video_rendition,
        segments_playlist_file=segments_playlist_file,
        segments=segment_paths,
    )

    assert video_rendition.playlist_file
    assert video_rendition.videorenditionsegment_set.count() == len(
        segment_paths
    )
    exp_prefix = f'videos/{video.id}/renditions/{video_rendition.id}/segments'
    exp_segment_numbers_and_filenames = (
        (
            0,
            f'{exp_prefix}/0.ts',
        ),
        (
            1,
            f'{exp_prefix}/1.ts',
        ),
        (
            2,
            f'{exp_prefix}/2.ts',
        ),
        (
            3,
            f'{exp_prefix}/3.ts',
        ),
        (
            4,
            f'{exp_prefix}/4.ts',
        ),
        (
            5,
            f'{exp_prefix}/5.ts',
        ),
        (
            6,
            f'{exp_prefix}/6.ts',
        ),
        (
            7,
            f'{exp_prefix}/7.ts',
        ),
        (
            8,
            f'{exp_prefix}/8.ts',
        ),
        (
            9,
            f'{exp_prefix}/9.ts',
        ),
        (
            10,
            f'{exp_prefix}/10.ts',
        ),
        (
            11,
            f'{exp_prefix}/11.ts',
        ),
        (
            12,
            f'{exp_prefix}/12.ts',
        ),
    )
    assert (
        tuple(
            video_rendition.videorenditionsegment_set.values_list(
                'segment_number', 'file'
            )
        )
        == exp_segment_numbers_and_filenames
    )


def test_get_rendition_playlists(video_with_renditions_and_segments, mocker):
    video, video_renditions_to_create = video_with_renditions_and_segments

    playlists = services._get_rendition_playlists(video_record=video)

    assert len(playlists) == 2
    exp_playlists = [
        {
            'height': 360,
            'playlist_url': mocker.ANY,
            'width': 640,
            'name': '360p',
            'resolution': '640x360',
            'bandwidth': 182464,
            'frame_rate': 30,
            'codecs_string': 'avc1.640028,mp4a.40.2',
        },
        {
            'height': 1080,
            'playlist_url': mocker.ANY,
            'width': 1920,
            'name': '1080p',
            'resolution': '1920x1080',
            'bandwidth': 5127303,
            'frame_rate': 30,
            'codecs_string': 'avc1.640028,mp4a.40.2',
        },
    ]
    assert playlists == exp_playlists
    assert all(p['playlist_url'].startswith('http') for p in playlists)


class TestGeneratePlaylist:
    def test(self, video_with_renditions_and_segments, mocker):
        video, _ = video_with_renditions_and_segments

        playlist_str = services.generate_master_playlist(video_id=video.id)

        playlist_data = m3u8.loads(playlist_str).data
        assert playlist_data == {
            'iframe_playlists': [],
            'is_endlist': False,
            'is_i_frames_only': False,
            'is_independent_segments': False,
            'is_variant': True,
            'keys': [],
            'media': [],
            'media_sequence': None,
            'part_inf': {},
            'playlist_type': None,
            'playlists': [
                {
                    'stream_info': {
                        'bandwidth': 182464,
                        'resolution': '640x360',
                        'closed_captions': 'NONE',
                        'codecs': 'avc1.640028,mp4a.40.2',
                        'program_id': 1,
                    },
                    'uri': mocker.ANY,
                },
                {
                    'stream_info': {
                        'bandwidth': 5127303,
                        'resolution': '1920x1080',
                        'closed_captions': 'NONE',
                        'codecs': 'avc1.640028,mp4a.40.2',
                        'program_id': 1,
                    },
                    'uri': mocker.ANY,
                },
            ],
            'rendition_reports': [],
            'segments': [],
            'session_data': [],
            'session_keys': [],
            'skip': {},
        }

    def test_returns_none_if_video_has_no_renditions(self, video):
        playlist_str = services.generate_master_playlist(video_id=video.id)

        assert playlist_str is None
