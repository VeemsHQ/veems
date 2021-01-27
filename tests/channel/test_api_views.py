from http.client import OK, NOT_FOUND, CREATED, BAD_REQUEST, FORBIDDEN
from pathlib import Path

from pytest_voluptuous import S
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from veems.channel import services

pytestmark = pytest.mark.django_db
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'
EXAMPLE_IMG = TEST_DATA_DIR / 'example-image.jpeg'
EXAMPLE_BANNER_IMG = TEST_DATA_DIR / 'example-banner.jpeg'


def test_get_channels(api_client, channel_factory, user_factory):
    api_client, user = api_client
    exp_channels = (
        channel_factory(user=user).id,
        channel_factory(user=user).id,
    )

    response = api_client.get('/api/v1/channel/')

    assert response.status_code == OK
    assert len(response.json()) == len(exp_channels)
    assert response.json()[0] == S(
        {
            'id': str,
            'user': user.id,
            'name': str,
            'description': str,
            'sync_videos_interested': bool,
            'language': 'en',
            'modified_on': str,
            'is_selected': bool,
            'followers_count': int,
            'avatar_image_small_url': str,
            'avatar_image_large_url': str,
            'banner_image_small_url': str,
            'banner_image_large_url': str,
            'has_banner': bool,
            'created_on': str,
            'created_date': str,
            'videos_count': int,
        }
    )
    assert all(c['id'] in exp_channels for c in response.json())


def test_get_channel(
    api_client,
    channel_factory,
    video_with_transcodes_factory,
    expected_video_resp_json,
):
    api_client, user = api_client
    channel = channel_factory(user=user)
    video_with_transcodes_factory(channel=channel)

    response = api_client.get(f'/api/v1/channel/{channel.id}/')

    assert response.status_code == OK
    resp_json = response.json()
    assert resp_json == S(
        {
            'id': channel.id,
            'user': user.id,
            'name': str,
            'description': str,
            'sync_videos_interested': bool,
            'language': 'en',
            'modified_on': str,
            'is_selected': bool,
            'followers_count': int,
            'avatar_image_small_url': str,
            'avatar_image_large_url': str,
            'banner_image_small_url': str,
            'banner_image_large_url': str,
            'has_banner': bool,
            'created_on': str,
            'created_date': str,
            'videos': list,
            'videos_count': int,
        }
    )
    assert len(resp_json['videos']) == 1
    assert resp_json['videos'][0] == expected_video_resp_json
    assert resp_json['videos'][0]['video_renditions']
    assert resp_json['videos'][0]['transcode_jobs']


class TestCreateChannel:
    @pytest.mark.parametrize('is_selected', [True, False])
    def test(self, api_client, is_selected):
        api_client, user = api_client

        body = {
            'name': 'my channel',
            'description': 'my desc',
            'sync_videos_interested': True,
            'is_selected': is_selected,
            'language': 'es',
        }
        response = api_client.post('/api/v1/channel/', body, format='json')

        assert response.status_code == CREATED
        resp_json = response.json()
        assert resp_json == S(
            {
                'id': str,
                'user': user.id,
                'name': body['name'],
                'description': body['description'],
                'sync_videos_interested': body['sync_videos_interested'],
                'language': body['language'],
                'modified_on': str,
                'is_selected': is_selected,
                'followers_count': int,
                'avatar_image_large_url': str,
                'avatar_image_small_url': str,
                'banner_image_small_url': str,
                'banner_image_large_url': str,
                'has_banner': bool,
                'created_on': str,
                'created_date': str,
                'videos_count': int,
            }
        )

    def test_returns_400_if_invalid_payload(self, api_client):
        api_client, user = api_client

        body = {
            # missing some values
            'name': 'my channel',
        }
        response = api_client.post('/api/v1/channel/', body, format='json')

        assert response.status_code == BAD_REQUEST
        assert response.json() == {
            'description': ['This field is required.'],
            'sync_videos_interested': ['This field is required.'],
        }


class TestUpdateChannel:
    @pytest.mark.parametrize(
        'body',
        [
            {
                'description': 'new desc',
                'sync_videos_interested': False,
            },
            {
                'name': 'new channel name',
                'description': 'new desc',
                'language': 'fr',
            },
            {
                'is_selected': True,
            },
        ],
    )
    def test(self, api_client, channel_factory, body):
        api_client, user = api_client
        channel_factory(user=user, is_selected=True)
        channel = channel_factory(user=user, is_selected=False)

        response = api_client.put(
            f'/api/v1/channel/{channel.id}/', body, format='json'
        )

        assert response.status_code == OK
        assert response.json() == S(
            {
                'id': channel.id,
                'user': user.id,
                'name': body.get('name', str),
                'description': body.get('description', str),
                'sync_videos_interested': body.get(
                    'sync_videos_interested', bool
                ),
                'language': body.get('language', str),
                'created_on': str,
                'modified_on': str,
                'is_selected': body.get('is_selected', channel.is_selected),
                'videos': list,
                'followers_count': int,
                'avatar_image_large_url': str,
                'avatar_image_small_url': str,
                'banner_image_small_url': str,
                'banner_image_large_url': str,
                'has_banner': bool,
                'created_on': str,
                'created_date': str,
                'videos_count': int,
            }
        )
        num_selected_channels = len(
            tuple(
                c
                for c in services.get_channels(user_id=user.id)
                if c.is_selected
            )
        )
        assert num_selected_channels == 1

    def test_returns_404_when_attempting_to_update_someone_elses_channel(
        self, api_client, channel_factory, user_factory
    ):
        api_client, user = api_client
        # Make a channel for the auth'd user
        channel_factory(user=user)
        # And one from someone else (which we'll try to update)
        channel = channel_factory(user=user_factory())

        response = api_client.put(
            f'/api/v1/channel/{channel.id}/',
            {
                'description': 'new desc',
            },
            format='json',
        )

        assert response.status_code == NOT_FOUND

    def test_cannot_update_user(
        self, api_client, channel_factory, user_factory
    ):
        api_client, user = api_client
        channel = channel_factory(user=user)
        another_user = user_factory()

        # Try to change the user who owns this channel
        body = {
            'description': 'new desc',
            'user': another_user.id,
        }
        response = api_client.put(
            f'/api/v1/channel/{channel.id}/', body, format='json'
        )

        assert response.status_code == OK
        assert response.json() == S(
            {
                'id': channel.id,
                # Check it wasn't updated
                'user': user.id,
                'name': channel.name,
                'description': body['description'],
                'sync_videos_interested': channel.sync_videos_interested,
                'language': channel.language,
                'created_on': str,
                'modified_on': str,
                'is_selected': True,
                'videos': list,
                'followers_count': int,
                'avatar_image_large_url': str,
                'avatar_image_small_url': str,
                'banner_image_small_url': str,
                'banner_image_large_url': str,
                'has_banner': bool,
                'created_on': str,
                'created_date': str,
                'videos_count': int,
            }
        )


class TestChannelAvatarAPIView:
    def test_get(self, api_client, channel_factory):
        api_client, user = api_client
        channel = channel_factory(user=user, avatar_image=None)

        response = api_client.get(f'/api/v1/channel/{channel.id}/avatar/')

        assert response.status_code == OK

        resp_json = response.json()
        assert resp_json == S(
            {
                'avatar_image_small_url': str,
                'avatar_image_large_url': str,
            }
        )
        assert resp_json['avatar_image_small_url']
        assert resp_json['avatar_image_large_url']
        # Check returned defaults
        assert 'defaults/' in resp_json['avatar_image_small_url']
        assert 'defaults/' in resp_json['avatar_image_large_url']

    def test_post(self, api_client, channel_factory):
        api_client, user = api_client
        channel = channel_factory(user=user)

        with EXAMPLE_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = api_client.post(
                f'/api/v1/channel/{channel.id}/avatar/', data=form_data
            )

        assert response.status_code == OK

        resp_json = response.json()
        assert resp_json == S(
            {
                'avatar_image_small_url': str,
                'avatar_image_large_url': str,
            }
        )
        assert resp_json['avatar_image_small_url']
        assert resp_json['avatar_image_large_url']

    def test_post_returns_404_when_attempting_to_update_other_users_avatar(
        self, api_client, channel_factory, user_factory
    ):
        api_client, user = api_client
        another_user = user_factory()
        channel = channel_factory(user=another_user)

        with EXAMPLE_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = api_client.post(
                f'/api/v1/channel/{channel.id}/avatar/', data=form_data
            )

        assert response.status_code == NOT_FOUND

    def test_post_returns_403_unauthenticated(
        self, client, api_client, channel_factory
    ):
        _, user = api_client
        channel = channel_factory(user=user)

        with EXAMPLE_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = client.post(
                f'/api/v1/channel/{channel.id}/avatar/', data=form_data
            )

        assert response.status_code == FORBIDDEN


class TestChannelBannerAPIView:
    def test_get(self, api_client, channel_factory):
        api_client, user = api_client
        channel = channel_factory(user=user, banner_image=None)

        response = api_client.get(f'/api/v1/channel/{channel.id}/banner/')

        assert response.status_code == OK

        resp_json = response.json()
        assert resp_json == S(
            {
                'banner_image_large_url': str,
            }
        )
        assert resp_json['banner_image_large_url']
        # Check returned defaults
        assert 'defaults/' in resp_json['banner_image_large_url']

    def test_post(self, api_client, channel_factory):
        api_client, user = api_client
        channel = channel_factory(user=user)

        with EXAMPLE_BANNER_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = api_client.post(
                f'/api/v1/channel/{channel.id}/banner/', data=form_data
            )

        assert response.status_code == OK

        resp_json = response.json()
        assert resp_json == S(
            {
                'banner_image_large_url': str,
            }
        )
        assert resp_json['banner_image_large_url']

    def test_post_returns_404_when_attempting_to_update_other_users_banner(
        self, api_client, channel_factory, user_factory
    ):
        api_client, user = api_client
        another_user = user_factory()
        channel = channel_factory(user=another_user)

        with EXAMPLE_BANNER_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = api_client.post(
                f'/api/v1/channel/{channel.id}/banner/', data=form_data
            )

        assert response.status_code == NOT_FOUND

    def test_post_returns_403_unauthenticated(
        self, client, api_client, channel_factory
    ):
        _, user = api_client
        channel = channel_factory(user=user)

        with EXAMPLE_BANNER_IMG.open('rb') as file_:
            form_data = {'file': SimpleUploadedFile(file_.name, file_.read())}
            response = client.post(
                f'/api/v1/channel/{channel.id}/banner/', data=form_data
            )

        assert response.status_code == FORBIDDEN
