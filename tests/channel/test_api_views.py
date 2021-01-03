from http.client import OK, NOT_FOUND, CREATED, BAD_REQUEST

from pytest_voluptuous import S
import pytest

pytestmark = pytest.mark.django_db


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
            'sync_videos_interested': True,
            'language': 'en',
            'created_on': str,
            'modified_on': str,
        }
    )
    assert all(c['id'] in exp_channels for c in response.json())


def test_get_channel(api_client, channel_factory):
    api_client, user = api_client
    channel = channel_factory(user=user)

    response = api_client.get(f'/api/v1/channel/{channel.id}/')

    assert response.status_code == OK
    assert response.json() == S(
        {
            'id': channel.id,
            'user': user.id,
            'name': str,
            'description': str,
            'sync_videos_interested': True,
            'language': 'en',
            'created_on': str,
            'modified_on': str,
        }
    )


class TestCreateChannel:
    def test(self, api_client):
        api_client, user = api_client

        body = {
            'name': 'my channel',
            'description': 'my desc',
            'sync_videos_interested': True,
            'language': 'es',
        }
        response = api_client.post('/api/v1/channel/', body, format='json')

        assert response.status_code == CREATED
        assert response.json() == S(
            {
                'id': str,
                'user': user.id,
                'name': body['name'],
                'description': body['description'],
                'sync_videos_interested': body['sync_videos_interested'],
                'language': body['language'],
                'created_on': str,
                'modified_on': str,
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
        assert response.json() == {'detail': 'Invalid payload'}


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
        ],
    )
    def test(self, api_client, channel_factory, body):
        api_client, user = api_client
        channel = channel_factory(user=user)

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
            }
        )

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
            }
        )
