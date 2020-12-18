import pytest
from pytest_voluptuous import S

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
    'video_path, exp_metadata', [
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
                            'minor_version': '0'
                        }
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
                        'width': 3840
                    },
                    'video_stream': {
                        'avg_frame_rate': '30/1',
                        'bit_rate': '43255196',
                        'bits_per_raw_sample': '8',
                        'chroma_location': 'left',
                        'closed_captions': 0,
                        'codec_long_name': (
                            'H.264 / AVC / MPEG-4 AVC / MPEG-4 part '
                            '10'
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
                            'visual_impaired': 0
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
                            'language': 'eng'
                        },
                        'time_base': '1/30000',
                        'width': 3840
                    }
                },
                required=False
            )
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
                            'visual_impaired': 0
                        },
                        'index': 1,
                        'r_frame_rate': '0/0',
                        'sample_fmt': 'fltp',
                        'sample_rate': '48000',
                        'start_pts': -7,
                        'start_time': '-0.007000',
                        'tags': {
                            'DURATION': '00:01:17.441000000',
                            'language': 'eng'
                        },
                        'time_base': '1/1000'
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
                        'tags': {
                            'ENCODER': 'Lavf58.45.100'
                        }
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
                        'width': 1080
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
                            'visual_impaired': 0
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
                            'language': 'eng'
                        },
                        'time_base': '1/1000',
                        'width': 1080
                    }
                },
                required=False
            )
        ),
    ]
)
def test_get_metadata(video_path, exp_metadata):
    metadata = services.get_metadata(video_path=video_path)

    assert metadata == exp_metadata
    assert sorted(metadata.keys()) == sorted(
        ('audio_stream', 'video_stream', 'summary', 'format')
    )


def test_persist_media_file_segments(video, simple_uploaded_file, tmpdir):
    media_file = models.MediaFile.objects.create(
        video=video,
        file=simple_uploaded_file,
        name='360p',
        ext='webm',
        file_size=1,
    )
    assert not media_file.hls_playlist_file
    video_path = constants.VIDEO_PATH_1080_30FPS_VERT
    profile = transcoder_profiles.Webm360p

    segment_hls_playlist, segment_paths = ffmpeg._create_segments_for_video(
        video_path=video_path,
        profile=profile,
        tmp_dir=tmpdir,
    )

    services.persist_media_file_segments(
        media_file=media_file,
        segments_playlist_file=segment_hls_playlist,
        segments=segment_paths,
    )

    assert media_file.hls_playlist_file
    assert media_file.mediafilesegment_set.count() == len(segment_paths)
    exp_segment_numbers_and_filenames = (
        (0, f'{media_file.id}/0.ts'), (1, f'{media_file.id}/1.ts'),
        (2, f'{media_file.id}/2.ts'), (3, f'{media_file.id}/3.ts'),
        (4, f'{media_file.id}/4.ts'), (5, f'{media_file.id}/5.ts'),
        (6, f'{media_file.id}/6.ts'), (7, f'{media_file.id}/7.ts'),
        (8, f'{media_file.id}/8.ts'), (9, f'{media_file.id}/9.ts'),
        (10, f'{media_file.id}/10.ts'), (11, f'{media_file.id}/11.ts'),
        (12, f'{media_file.id}/12.ts')
    )
    assert tuple(
        media_file.mediafilesegment_set.values_list('segment_number', 'file')
    ) == exp_segment_numbers_and_filenames


def test_get_rendition_playlists(video, simple_uploaded_file, tmpdir, mocker):
    media_files_to_create = (
        (640, 360, constants.VID_360P_24FPS),
        (1920, 1920, constants.VIDEO_PATH_1080_60FPS),
    )
    for width, height, video_path in media_files_to_create:
        media_file = models.MediaFile.objects.create(
            video=video,
            file=simple_uploaded_file,
            name=f'{height}p',
            ext='webm',
            file_size=1,
            width=width,
            height=height,
            metadata=services.get_metadata(video_path),
        )
        assert not media_file.hls_playlist_file
        video_path = constants.VIDEO_PATH_1080_30FPS_VERT
        profile = transcoder_profiles.Webm360p
        segment_hls_playlist, segment_paths = ffmpeg._create_segments_for_video(
            video_path=video_path,
            profile=profile,
            tmp_dir=tmpdir,
        )
        services.persist_media_file_segments(
            media_file=media_file,
            segments_playlist_file=segment_hls_playlist,
            segments=segment_paths,
        )

    playlists = services.get_rendition_playlists(video_record=video)

    assert len(playlists) == len(media_files_to_create)
    exp_playlists = [
        {
            'codec': 'h264.avc1.High.30',
            'height': 360,
            'playlist_url': mocker.ANY,
            'width': 640
        }, {
            'codec': 'h264.avc1.High.42',
            'height': 1920,
            'playlist_url': mocker.ANY,
            'width': 1920
        }
    ]
    assert playlists == exp_playlists
