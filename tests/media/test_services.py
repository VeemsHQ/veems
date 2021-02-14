from pathlib import Path
import shutil

import pytest
from pytest_voluptuous import S
from django.core.files import File
import m3u8
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from veems.media import services, models
from veems.media.transcoder.transcoder_executor import ffmpeg
from veems.media.transcoder import transcoder_profiles
from tests import constants

pytestmark = pytest.mark.django_db
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'


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
        name='webm_360p',
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
    assert video_rendition.rendition_segments.count() == len(segment_paths)
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
            video_rendition.rendition_segments.values_list(
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


class TestGetVideo:
    def test(self, video):
        result = services.get_video(id=video.id)

        assert isinstance(result, models.Video)
        assert result == video

    def test_not_found_if_is_deleted(self, video):
        services.delete_video(id=video.id)

        with pytest.raises(ObjectDoesNotExist):
            services.get_video(id=video.id)

    def test_found_if_is_deleted_and_include_deleted_true(self, video):
        services.delete_video(id=video.id)

        result = services.get_video(id=video.id, include_deleted=True)

        assert isinstance(result, models.Video)
        assert result == video


def test_delete_video(video):
    video = services.delete_video(id=video.id)

    assert video.deleted_on


def test_get_popular_videos(
    video_with_transcodes_factory, channel_factory, user_factory
):
    visibility_values = (
        'private',
        'public',
        'public',
        'public',
        'public',
        'unlisted',
    )
    is_viewable_values = (False, False, True, True, True, True)
    deleted_on_values = (None, None, None, None, timezone.now(), None)
    for visibility, is_viewable, deleted_on in zip(
        visibility_values, is_viewable_values, deleted_on_values
    ):
        user = user_factory()
        channel = channel_factory(user=user)
        video_with_transcodes_factory(
            channel=channel,
            visibility=visibility,
            is_viewable=is_viewable,
            deleted_on=deleted_on,
        )

    records = services.get_popular_videos()

    assert all(isinstance(r, models.Video) for r in records)
    assert len(records) == 2
    assert all(
        r.visibility == 'public' and r.is_viewable is True and not r.deleted_on
        for r in records
    )
    assert records[0].created_on > records[1].created_on


def test_mark_video_as_viewable(video_factory):
    video = video_factory(is_viewable=False)

    updated_video = services.mark_video_as_viewable(video=video)

    assert updated_video.is_viewable is True


def test_create_video(upload):
    video = services.create_video(upload=upload, title='hello')

    assert video.channel == upload.channel
    assert video.upload == upload
    assert video.title == 'hello'
    assert video.description is None
    assert not video.default_thumbnail_image
    assert video.default_thumbnail_image_small_url
    assert video.default_thumbnail_image_medium_url
    assert video.default_thumbnail_image_large_url


class TestGetVideos:
    def test(self, video_factory):
        videos = (
            video_factory(),
            video_factory(),
            video_factory(),
        )
        # Deleted videos shouldn't be returned
        services.delete_video(id=videos[-1].id)
        # Non-public videos shouldn't be returned
        video_factory(visibility='draft')
        video_factory(visibility='private')
        video_factory(visibility='unlisted')

        records = services.get_videos()

        assert tuple(records) == tuple(videos[:-1])
        assert all(not v.deleted_on for v in records)

    def test_with_channel_id_and_user_id_of_owner_returns_non_public(
        self, video_factory, channel_factory, user
    ):
        channel = channel_factory(user=user)
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel)
        video_factory(channel=channel)
        # Deleted videos shouldn't be returned
        services.delete_video(id=video_factory(channel=channel).id)
        # Non-public videos should be returned
        video_factory(channel=channel, visibility='private')
        video_factory(channel=channel, visibility='unlisted')
        video_factory(channel=channel, visibility='draft')

        records = services.get_videos(channel_id=channel.id, user_id=user.id)

        assert len(records) == 5
        # Check non public were returned
        assert set(r.visibility for r in records) == {
            'public',
            'private',
            'unlisted',
            'draft',
        }

    def test_with_channel_id_and_user_id_of_non_owner_returns_only_public(
        self, video_factory, user_factory, channel_factory, user
    ):
        channel = channel_factory(user=user)
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel)
        video_factory(channel=channel)
        # Deleted videos shouldn't be returned
        services.delete_video(id=video_factory(channel=channel).id)
        # Non-public videos shouldn't be returned
        video_factory(channel=channel, visibility='private')
        video_factory(channel=channel, visibility='unlisted')
        video_factory(channel=channel, visibility='draft')

        records = services.get_videos(
            channel_id=channel.id, user_id=user_factory().id
        )

        assert len(records) == 2
        # Check public were returned
        assert set(r.visibility for r in records) == {
            'public',
        }

    def test_with_channel_id(self, video_factory, channel_factory, user):
        channel = channel_factory(user=user)
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel_factory(user=user))
        video_factory(channel=channel)
        video_factory(channel=channel)
        # Deleted videos shouldn't be returned
        services.delete_video(id=video_factory(channel=channel).id)
        # Non-public videos shouldn't be returned
        video_factory(channel=channel, visibility='private')
        video_factory(channel=channel, visibility='unlisted')
        video_factory(channel=channel, visibility='draft')

        records = services.get_videos(channel_id=channel.id)

        assert len(records) == 2
        assert all(
            v.channel_id == channel.id and not v.deleted_on for v in records
        )


def test_generate_default_thumbnail_image(tmpdir):
    image_path = TEST_DATA_DIR / 'thumbnail-vertical.jpg'
    test_image_path = tmpdir / 'thumbnail-vertical.jpg'
    shutil.copyfile(image_path, test_image_path)

    result_image = services._generate_default_thumbnail_image(
        image_path=test_image_path
    )

    assert result_image.exists()
    metadata = services.get_metadata(result_image)
    assert metadata['summary']['width'] == 1280
    assert metadata['summary']['height'] == 720


def test_set_video_default_thumbnail_image(video, tmpdir):
    image_path = TEST_DATA_DIR / 'thumbnail-vertical.jpg'
    test_image_path = tmpdir / 'thumbnail-vertical.jpg'
    shutil.copyfile(image_path, test_image_path)
    assert not video.default_thumbnail_image
    thumbnail_paths = (
        test_image_path,
        test_image_path,
        test_image_path,
    )

    updated_video_record = services.set_video_default_thumbnail_image(
        thumbnail_paths=thumbnail_paths,
        video_record=video,
    )

    assert updated_video_record.id == video.id
    assert updated_video_record.default_thumbnail_image


def test_set_video_custom_thumbnail_image(video, tmpdir):
    image_path = TEST_DATA_DIR / 'thumbnail-vertical.jpg'
    test_image_path = tmpdir / 'thumbnail-vertical.jpg'
    shutil.copyfile(image_path, test_image_path)

    with test_image_path.open('rb') as file_:
        video = services.set_video_custom_thumbnail_image(
            video_record=video, thumbnail_image=File(file_)
        )

    assert video.custom_thumbnail_image


def test_video_like(video, user):
    for _ in range(2):
        likedislike = services.video_like(video_id=video.id, user_id=user.id)

    assert likedislike.is_like is True
    assert likedislike.video == video
    assert likedislike.user == user
    assert len(services.get_video_likedislikes(video_id=video.id)) == 1


def test_video_remove_likedislike(video, user):
    services.video_like(video_id=video.id, user_id=user.id)
    services.video_dislike(video_id=video.id, user_id=user.id)

    likedislike = services.video_remove_likedislike(
        video_id=video.id, user_id=user.id
    )

    assert likedislike.is_like is None
    assert likedislike.video == video
    assert likedislike.user == user
    assert len(services.get_video_likedislikes(video_id=video.id)) == 1


def test_video_dislike(video, user):
    for _ in range(2):
        likedislike = services.video_dislike(
            video_id=video.id, user_id=user.id
        )

    assert likedislike.is_like is False
    assert likedislike.video == video
    assert likedislike.user == user
    assert len(services.get_video_likedislikes(video_id=video.id)) == 1


def test_get_video_likedislike_count(video, user_factory):
    for _ in range(2):
        services.video_like(video_id=video.id, user_id=user_factory().id)
    for _ in range(3):
        services.video_dislike(video_id=video.id, user_id=user_factory().id)

    result = services.get_video_likedislike_count(video_id=video.id)

    assert result == {
        'like_count': 2,
        'dislike_count': 3,
    }


def test_get_video_likedislike(video, user):
    services.video_like(video_id=video.id, user_id=user.id)

    record = services.get_video_likedislike(user_id=user.id, video_id=video.id)

    assert record
    assert isinstance(record, services.models.VideoLikeDislike)
    assert record.is_like is True
    assert record.video == video
    assert record.user == user


def test_set_video_custom_thumbnail_image_from_rendition_thumbnail(
    video, rendition_thumbnail
):
    assert not video.custom_thumbnail_image

    updated_video, thumbnail_path = (
        services.set_video_custom_thumbnail_image_from_rendition_thumbnail(
            video_record=video,
            video_rendition_thumbnail_id=rendition_thumbnail.id,
            delete_tempfile=False,
        )
    )

    # TODO: tests with diff input res, assert on output img res.
    assert updated_video.custom_thumbnail_image
    metadata = services.get_metadata(thumbnail_path)
    assert metadata['summary']['width'] == transcoder_profiles.Webm144p.width
    assert metadata['summary']['height'] == transcoder_profiles.Webm144p.height
