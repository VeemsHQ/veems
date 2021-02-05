from uuid import uuid4
from pathlib import Path

import pytest
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from pytest_voluptuous import S
from rest_framework.test import APIClient

from veems.channel import services as channel_services
from veems.media.transcoder import transcoder_profiles
from veems.media.transcoder.transcoder_executor import ffmpeg
from veems.media import models, services as media_services
from tests import constants


TEST_DATA_DIR = Path(__file__).parent / 'test_data'
EXAMPLE_IMG = TEST_DATA_DIR / 'example-image.jpeg'
VIDEO_PATH = constants.VID_360P_24FPS
VIDEO_PATH_2160_30FPS = TEST_DATA_DIR / '2160p_30fps.mp4'


@pytest.fixture
def simple_uploaded_img_file():
    with EXAMPLE_IMG.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(EXAMPLE_IMG.name, file_contents)


@pytest.fixture
def simple_uploaded_img_file_factory():
    def make(path=EXAMPLE_IMG):
        with path.open('rb') as file_:
            file_contents = file_.read()
        return SimpleUploadedFile(path.name, file_contents)

    return make


@pytest.fixture
def pasword():
    return f'password{str(uuid4())[:5]}'


@pytest.fixture
def user_factory(pasword):
    def make():
        unique = f'user{str(uuid4())[:5]}'
        email = f'{unique}@veems.tv'
        user = get_user_model()(
            username=email,
            email=email,
        )
        user.set_password(pasword)
        user.save()
        return user

    return make


@pytest.fixture
def user(user_factory):
    return user_factory()


@pytest.fixture
def channel_factory():
    def make(
        *,
        user,
        description=None,
        name=None,
        avatar_image=None,
        banner_image=None,
        is_selected=True,
    ):
        return channel_services.create_channel(
            name=name or 'My Channel',
            user=user,
            description=description or 'x' * 5000,
            sync_videos_interested=True,
            language='en',
            avatar_image=avatar_image,
            banner_image=banner_image,
            is_selected=is_selected,
        )

    return make


@pytest.fixture
def channel(user, channel_factory):
    return channel_factory(user=user)


@pytest.fixture
def api_client(user_factory):
    user = user_factory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def api_client_factory(user_factory):
    def make(user=None):
        user = user or user_factory()
        client = APIClient()
        client.force_authenticate(user=user)
        return client, user

    return make


@pytest.fixture
def api_client_no_auth():
    return APIClient()


@pytest.fixture
def video_with_transcodes_factory(
    video_factory,
    transcode_job_factory,
    simple_uploaded_file_factory,
    rendition_playlist_file,
):
    def make(channel, visibility='public', **video_kwargs):
        user = channel.user
        video = video_factory(
            channel=channel,
            video_path=VIDEO_PATH,
            description='description',
            tags=['tag1', 'tag2'],
            visibility=visibility,
            title='title',
            duration=10,
            framerate=30,
            **video_kwargs,
        )
        transcode_job = transcode_job_factory(
            profile='144p', video_record=video
        )
        transcode_job2 = transcode_job_factory(
            profile='360p', video_record=video
        )
        file_ = simple_uploaded_file_factory(video_path=VIDEO_PATH_2160_30FPS)
        playlist_file = rendition_playlist_file.close()
        try:
            playlist_file = rendition_playlist_file.open()
        except ValueError:
            rendition_playlist_file.close()
        try:
            rendition_playlist_file.seek(0)
        except ValueError:
            pass
        video_rendition = models.VideoRendition.objects.create(
            video=video,
            file=file_.open(),
            playlist_file=playlist_file,
            file_size=1000,
            width=256,
            height=144,
            duration=10,
            ext='webm',
            container='webm',
            audio_codec='opus',
            video_codec='vp9',
            name='144p',
            framerate=30,
            metadata={'example': 'metadata'},
        )
        return {
            'video': video,
            'transcode_job': transcode_job,
            'transcode_job2': transcode_job2,
            'video_rendition': video_rendition,
            'user': user,
        }

    return make


@pytest.fixture
def upload(upload_factory):
    return upload_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def video(video_factory):
    return video_factory(video_path=VIDEO_PATH_2160_30FPS)


@pytest.fixture
def simple_uploaded_file():
    with VIDEO_PATH_2160_30FPS.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(VIDEO_PATH_2160_30FPS.name, file_contents)


@pytest.fixture
def rendition_playlist_file():
    with constants.RENDITION_PLAYLIST.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(constants.RENDITION_PLAYLIST.name, file_contents)


@pytest.fixture
def simple_uploaded_file_factory():
    def make(video_path):

        with video_path.open('rb') as file_:
            file_contents = file_.read()
        return SimpleUploadedFile(VIDEO_PATH_2160_30FPS.name, file_contents)

    return make


@pytest.fixture
def upload_factory(request):
    def make(video_path=VIDEO_PATH_2160_30FPS, channel=None):
        with video_path.open('rb') as file_:
            file_contents = file_.read()
        channel = channel or request.getfixturevalue('channel')
        upload = models.Upload.objects.create(
            presigned_upload_url='https://example.com/s3-blah',
            media_type='video',
            file=SimpleUploadedFile(video_path.name, file_contents),
            channel=channel,
        )
        return upload

    return make


@pytest.fixture
def video_factory(upload_factory, request):
    def make(video_path=VIDEO_PATH, channel=None, **kwargs):
        channel = channel or request.getfixturevalue('channel')
        upload = upload_factory(video_path=video_path, channel=channel)
        return models.Video.objects.create(
            upload=upload, channel=channel, **kwargs
        )

    return make


@pytest.fixture
def transcode_job_factory(request):
    def make(profile, status='created', video_record=None):
        return models.TranscodeJob.objects.create(
            video=video_record or request.getfixturevalue('video'),
            profile=profile,
            executor='ffmpeg',
            status=status,
            started_on=timezone.now(),
        )

    return make


@pytest.fixture
def transcode_job(transcode_job_factory):
    return transcode_job_factory(profile='webm_360p')


@pytest.fixture
def video_with_renditions_and_segments(video, simple_uploaded_file, tmpdir):
    video_renditions_to_create = (
        (640, 360, constants.VID_360P_24FPS, False),
        (640, 360, constants.VID_360P_24FPS, True),
        (1920, 1080, constants.VIDEO_PATH_1080_60FPS, True),
    )
    for (
        width,
        height,
        video_path,
        create_segments,
    ) in video_renditions_to_create:
        video_rendition = models.VideoRendition.objects.create(
            video=video,
            file=simple_uploaded_file,
            name=f'{height}p',
            ext='webm',
            framerate=30,
            file_size=1,
            width=width,
            height=height,
            metadata=media_services.get_metadata(video_path),
            codecs_string='avc1.640028,mp4a.40.2',
        )
        assert not video_rendition.playlist_file
        if not create_segments:
            continue
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
        media_services.persist_video_rendition_segments(
            video_rendition=video_rendition,
            segments_playlist_file=segments_playlist_file,
            segments=segment_paths,
        )
    return video, video_renditions_to_create


@pytest.fixture
def expected_channel_resp_json():
    return S(
        {
            'avatar_image_large_url': str,
            'avatar_image_small_url': str,
            'banner_image_large_url': str,
            'banner_image_small_url': str,
            'created_date': str,
            'created_on': str,
            'description': str,
            'followers_count': int,
            'has_banner': bool,
            'id': str,
            'is_selected': bool,
            'language': 'en',
            'modified_on': str,
            'name': str,
            'sync_videos_interested': bool,
            'user': str,
            'videos_count': int,
        }
    )


@pytest.fixture
def expected_video_resp_json():
    return S(
        {
            'channel_avatar_image_small_url': str,
            'channel_id': str,
            'channel_name': str,
            'channel': str,
            'comment_count': int,
            'created_date_human': str,
            'created_date': str,
            'thumbnail_image_small_url': str,
            'thumbnail_image_medium_url': str,
            'thumbnail_image_large_url': str,
            'description': str,
            'dislikes_count': int,
            'duration_human': str,
            'duration': int,
            'id': str,
            'likes_count': int,
            'playlist_file': str,
            'tags': list,
            'time_ago_human': str,
            'title': str,
            'transcode_jobs': list,
            'video_renditions_count': int,
            'video_renditions': list,
            'view_count': int,
            'visibility': str,
            'authenticated_user_data': dict,
            'likesdislikes_percentage': float,
        }
    )


@pytest.fixture
def expected_video_slim_resp_json():
    return S(
        {
            'channel_avatar_image_small_url': str,
            'channel_id': str,
            'channel_name': str,
            'channel': str,
            'comment_count': int,
            'created_date_human': str,
            'created_date': str,
            'thumbnail_image_small_url': str,
            'thumbnail_image_medium_url': str,
            'thumbnail_image_large_url': str,
            'description': str,
            'duration_human': str,
            'duration': int,
            'id': str,
            'tags': ['tag1', 'tag2'],
            'time_ago_human': str,
            'title': str,
            'video_renditions_count': int,
            'view_count': int,
            'visibility': str,
        }
    )
