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
        vid_ctx = response.context['video']
        assert vid_ctx['id'] == video.id
        assert vid_ctx['title'] == video.title
        assert vid_ctx['video_renditions_count'] == 1
        assert vid_ctx['description'] == video.description
        assert vid_ctx['created_date'] == video.created_on.date()
        assert vid_ctx['view_count'] == 0
        assert vid_ctx['comment_count'] == 0
        assert vid_ctx['tags'] == ['tag1', 'tag2']
        assert vid_ctx['playlist_file'] == reverse(
            'api-video-playlist', args=[video.id]
        )
        channel_ctx = response.context['channel']
        assert channel_ctx['name'] == channel.name
        assert channel_ctx['id'] == channel.id
        assert channel_ctx['followers_count'] == 0
        assert channel_ctx['description'] == channel.description
        assert (
            channel_ctx['avatar_image_small_url'].split('?')[0]
            == channel.avatar_image_small_url.split('?')[0]
        )
        assert (
            channel_ctx['banner_image_small_url'].split('?')[0]
            == channel.banner_image_small_url.split('?')[0]
        )
