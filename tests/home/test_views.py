from http.client import OK
from datetime import date

from pytest_voluptuous import S
import pytest

pytestmark = pytest.mark.django_db


class TestIndexView:
    def test(
        self, client, video_with_transcodes_factory, channel_factory, user
    ):
        channel = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public',
            is_viewable=True
        )
        video_with_transcodes_factory(
            channel=channel, visibility='public',
            is_viewable=True
        )

        response = client.get('/')

        assert response.status_code == OK
        assert len(response.context['videos_popular']) == 2
        video = response.context['videos_popular'][0]
        assert video['duration'] is not None
        assert video == S(
            {
                'id': str,
                'channel': str,
                'channel_id': str,
                'channel_name': str,
                'comment_count': int,
                'created_date': date,
                'description': str,
                'duration': int,
                'duration_human': str,
                'tags': ['tag1', 'tag2'],
                'thumbnail': str,
                'time_ago_human': str,
                'title': str,
                'video_renditions_count': int,
                'view_count': int,
                'visibility': str,
            }
        )
