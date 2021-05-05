from http.client import OK

import pytest

pytestmark = pytest.mark.django_db


class TestVideosView:
    def test(
        self,
        client,
        video_with_transcodes_factory,
        channel_factory,
        user,
        password,
        expected_video_resp_json,
    ):
        assert client.login(username=user.email, password=password)
        # Select a channel and add videos
        channel = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
            is_selected=True,
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public', is_viewable=True
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public', is_viewable=True
        )
        assert user.channels.count() == 1
        # Add another unselected channel with videos
        channel_2 = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
            is_selected=False,
        )
        video_with_transcodes_factory(
            channel=channel_2, visibility='public', is_viewable=True
        )

        response = client.get('/channel/videos/')

        assert response.status_code == OK
        assert response.context['channel_id'] == channel.id
        assert len(response.context['channel_videos']) == 2
        for video in response.context['channel_videos']:
            assert video == expected_video_resp_json
            # Check only videos for the selected channel are listed
            assert video['channel_id'] == channel.id


class TestCustomizationView:

    pass
