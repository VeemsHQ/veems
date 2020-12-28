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
