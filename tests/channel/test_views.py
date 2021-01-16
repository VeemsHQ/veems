from http.client import OK

from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db


class TestVideoView:
    def test(
        self, client, video_with_transcodes_factory, channel_factory, user
    ):
        channel = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
        )
        video_data = video_with_transcodes_factory(channel=channel)
        video = video_data['video']

        response = client.get(f'/v/{video.id}/')

        assert response.status_code == OK
        assert response.context['video_id'] == video.id
        assert response.context['video_title'] == video.title
        assert response.context['video_rendition_count'] == 1
        assert response.context['video_description'] == video.description
        assert (
            response.context['video_created_date'] == video.created_on.date()
        )
        assert response.context['video_view_count'] == 0
        assert response.context['video_comment_count'] == 0
        assert response.context['video_playlist_url'] == reverse(
            'api-video-playlist', args=[video.id]
        )
        assert response.context['channel_name'] == channel.name
        assert response.context['channel_id'] == channel.id
        assert response.context['channel_followers_count'] == 0
        assert response.context['channel_description'] == channel.description
        assert (
            response.context['channel_avatar_image_small_url']
            == channel.avatar_image_small_url
        )
        assert (
            response.context['channel_banner_image_small_url']
            == channel.banner_image_small_url
        )
