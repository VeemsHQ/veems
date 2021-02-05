import pytest

from veems.channel import serializers

pytestmark = pytest.mark.django_db


class TestChannelSerializer:
    def test_get_videos_count(self, channel, video_factory):
        video_factory(channel=channel)
        video_factory(channel=channel)

        data = serializers.ChannelSerializer(
            user_id=channel.user_id, instance=channel
        ).data

        assert data['videos_count'] == 2
