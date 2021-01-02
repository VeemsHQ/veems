import pytest

from veems.channel import services

pytestmark = pytest.mark.django_db


def test_create_channel(user, channel):
    assert isinstance(channel, services.models.Channel)
    assert channel.name == 'My Channel'
    assert channel.user == user
    assert channel.description == 'x' * 5000
    assert channel.sync_videos_interested is True


def test_get_channel(user, channel):
    record = services.get_channel(id=channel.id)

    assert record.id == channel.id
    assert isinstance(record, services.models.Channel)


class TestGetChannels:

    def test(self, user_factory, channel_factory):
        channel_factory(user=user_factory())
        channel_factory(user=user_factory())

        records = services.get_channels()

        assert len(records) == 2
        assert all(isinstance(c, services.models.Channel) for c in records)

    def test_with_user_id(self, user_factory, channel_factory):
        user = user_factory()
        channel_factory(user=user)
        channel_factory(user=user)
        channel_factory(user=user_factory())

        records = services.get_channels(user_id=user.id)

        assert len(records) == 2
        assert all(c.user_id == user.id for c in records)
