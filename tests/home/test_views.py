from http.client import OK

import pytest

pytestmark = pytest.mark.django_db


class TestIndexView:
    def test(
        self,
        client,
        video_with_transcodes_factory,
        channel_factory,
        user,
        expected_video_slim_resp_json,
    ):
        channel = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public', is_viewable=True
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public', is_viewable=True
        )

        response = client.get('/')

        assert response.status_code == OK
        assert len(response.context['videos_popular']) == 2
        video = response.context['videos_popular'][0]
        assert video['duration'] is not None
        assert video == expected_video_slim_resp_json
