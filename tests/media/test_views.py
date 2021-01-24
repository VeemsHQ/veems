from http.client import OK

from django.urls import reverse
import pytest

from veems.media import services

pytestmark = pytest.mark.django_db


class TestVideoView:
    def test(
        self,
        client,
        video_with_transcodes_factory,
        channel_factory,
        user,
        user_factory,
        expected_video_resp_json,
        expected_channel_resp_json,
    ):
        channel = channel_factory(
            name='My Channel',
            user=user,
            description='My Channel Desc',
        )
        video_data = video_with_transcodes_factory(channel=channel)
        video = video_data['video']
        services.video_dislike(video_id=video.id, user_id=user.id)
        services.video_like(video_id=video.id, user_id=user_factory().id)

        response = client.get(f'/v/{video.id}/')

        assert response.status_code == OK
        video_context = response.context['video']
        expected_video_context = {
            'id': video.id,
            'title': video.title,
            'video_renditions_count': 1,
            'description': video.description,
            'created_date': video.created_on.date().isoformat(),
            'playlist_file': reverse('api-video-playlist', args=[video.id]),
            'likes_count': 1,
            'dislikes_count': 1,
        }
        expected_video_resp_json = expected_video_resp_json.extend(
            expected_video_context
        )
        assert dict(video_context) == expected_video_resp_json
        channel_context = response.context['channel']
        expected_channel_context = {
            'name': channel.name,
            'id': channel.id,
            'description': channel.description,
        }
        expected_channel_resp_json = expected_channel_resp_json.extend(
            expected_channel_context
        )
        assert dict(channel_context) == expected_channel_resp_json
        assert (
            channel_context['avatar_image_small_url'].split('?')[0]
            == channel.avatar_image_small_url.split('?')[0]
        )
        assert (
            channel_context['banner_image_small_url'].split('?')[0]
            == channel.banner_image_small_url.split('?')[0]
        )

    def test_logged_in_and_has_disliked_video(
        self,
        client,
        video_with_transcodes_factory,
        channel,
        user,
        expected_video_resp_json,
        expected_channel_resp_json,
    ):
        video_data = video_with_transcodes_factory(channel=channel)
        video = video_data['video']
        services.video_dislike(video_id=video.id, user_id=user.id)
        client.force_login(user=user)

        response = client.get(f'/v/{video.id}/')

        assert response.status_code == OK
        video_context = response.context['video']
        expected_video_context = {
            'id': video.id,
            'likes_count': 0,
            'dislikes_count': 1,
            'authenticated_user_data': {
                'has_liked_video': False,
            },
        }
        expected_video_resp_json = expected_video_resp_json.extend(
            expected_video_context
        )
        assert dict(video_context) == expected_video_resp_json
        channel_context = response.context['channel']
        assert dict(channel_context) == expected_channel_resp_json

    def test_logged_in(
        self,
        client,
        video_with_transcodes_factory,
        channel,
        user,
        expected_video_resp_json,
        expected_channel_resp_json,
    ):
        video_data = video_with_transcodes_factory(channel=channel)
        video = video_data['video']
        client.force_login(user=user)

        response = client.get(f'/v/{video.id}/')

        assert response.status_code == OK
        video_context = response.context['video']
        expected_video_context = {
            'id': video.id,
            'likes_count': 0,
            'dislikes_count': 0,
            'authenticated_user_data': {},
        }
        expected_video_resp_json = expected_video_resp_json.extend(
            expected_video_context
        )
        assert dict(video_context) == expected_video_resp_json
        channel_context = response.context['channel']
        assert dict(channel_context) == expected_channel_resp_json
