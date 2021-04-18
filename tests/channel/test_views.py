from http.client import OK

from pytest_voluptuous import S
import pytest

pytestmark = pytest.mark.django_db


class TestChannelIndexView:
    def test(
        self,
        client,
        video_with_transcodes_factory,
        channel_factory,
        user,
        expected_channel_resp_json,
    ):
        for channel_name in ('My channel 1', 'My channel 2'):
            channel = channel_factory(
                name=channel_name,
                user=user,
                description=f'{channel_name} Desc',
            )
            video_with_transcodes_factory(
                channel=channel, visibility='public', is_viewable=True
            )
            video_with_transcodes_factory(
                channel=channel, visibility='public', is_viewable=True
            )

        response = client.get(f'/c/{channel.id}/')

        assert response.status_code == OK
        assert len(response.context['channel_videos']) == 2
        assert all(
            v['channel_id'] == channel.id
            for v in response.context['channel_videos']
        )
        expected = expected_channel_resp_json
        expected = expected_channel_resp_json.extend({'id': channel.id})
        assert dict(response.context['channel']) == expected
        assert response.context['is_owner'] is False
        assert len(response.context['channel_videos']) == 2


class TestChannelAboutView:
    def test(
        self, client, video_with_transcodes_factory, channel_factory, user
    ):
        for channel_name in ('My channel 1', 'My channel 2'):
            channel = channel_factory(
                name=channel_name,
                user=user,
                description=f'{channel_name} Desc',
            )
            video_with_transcodes_factory(
                channel=channel, visibility='public', is_viewable=True
            )
            video_with_transcodes_factory(
                channel=channel, visibility='public', is_viewable=True
            )

        response = client.get(f'/c/{channel.id}/about/')

        assert response.status_code == OK
        assert dict(response.context['channel']) == S(
            {
                'avatar_image_large_url': str,
                'avatar_image_small_url': str,
                'banner_image_large_url': str,
                'banner_image_small_url': str,
                'created_date': str,
                'created_on': str,
                'description': str,
                'followers_count': 0,
                'has_banner': bool,
                'id': channel.id,
                'is_selected': bool,
                'language': str,
                'modified_on': str,
                'name': str,
                'sync_videos_interested': bool,
                'user': str,
                'videos_count': int,
            }
        )
        assert response.context['is_owner'] is False


class TestCustomizationView:
    @pytest.fixture(autouse=True)
    def setup(self, client, user, password, channel_factory):
        channel = channel_factory(user=user, is_selected=True)
        assert client.login(username=user.email, password=password)
        self.channel = channel

    def test_get(self, client):
        response = client.get('/channel/customization/')

        assert response.status_code == OK
        assert response.context['selected_channel'] == self.channel.id

    def test_post_channel_name(self, client):
        response = client.post('/channel/customization/', data={})

        assert response.status_code == OK

    def test_post_channel_description(self):
        pass

    def test_post_avatar_image(self):
        pass

    def test_post_banner_image(self):
        pass
