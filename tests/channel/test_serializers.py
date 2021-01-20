import pytest

from veems.channel import serializers

pytestmark = pytest.mark.django_db


class TestChannelSerializer:
    def test_get_videos_count(self, channel, video_factory):
        video_factory(channel=channel)
        video_factory(channel=channel)

        data = serializers.ChannelSerializer(instance=channel).data

        assert data['videos_count'] == 2
