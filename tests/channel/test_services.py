import pytest

from veems.channel import services

pytestmark = pytest.mark.django_db


def test_create_channel(user):
    record = services.create_channel(
        name='My Channel',
        user=user,
        description='x' * 5000,
        sync_videos_interested=True,
    )

    assert isinstance(record, services.models.Channel)
    assert record.name == 'My Channel'
    assert record.user == user
    assert record.description == 'x' * 5000
    assert record.sync_videos_interested is True


def test_get_channel(user):
    existing_channel = services.create_channel(
        name='My Channel',
        user=user,
        description='x' * 5000,
        sync_videos_interested=True,
    )

    record = services.get_channel(id=existing_channel.id)

    assert record.id == existing_channel.id
    assert isinstance(record, services.models.Channel)
