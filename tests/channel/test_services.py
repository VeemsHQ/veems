from pathlib import Path

import pytest

from veems.channel import services

pytestmark = pytest.mark.django_db
TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'
EXAMPLE_BANNER_IMG = TEST_DATA_DIR / 'example-banner.jpeg'


class TestCreateChannel:

    def test(self, user, simple_uploaded_img_file_factory):
        channel = services.create_channel(
            name='My Channel',
            user=user,
            description='x' * 5000,
            sync_videos_interested=True,
            language='en',
            avatar_image=simple_uploaded_img_file_factory(),
            banner_image=simple_uploaded_img_file_factory(
                path=EXAMPLE_BANNER_IMG
            ),
        )

        assert isinstance(channel, services.models.Channel)
        assert channel.name == 'My Channel'
        assert channel.user == user
        assert channel.description == 'x' * 5000
        assert channel.sync_videos_interested is True
        # Original avatar
        assert channel.avatar_image.url
        assert channel.avatar_image.width == 828
        assert channel.avatar_image.height == 663
        # Small avatar
        try:
            channel.avatar_image_small.open()
        except ValueError:
            pass
        assert channel.avatar_image_small.url == channel.avatar_image_small_url
        assert channel.avatar_image_small.width == 44
        assert channel.avatar_image_small.height == 44
        # Large avatar
        try:
            channel.avatar_image_large.open()
        except ValueError:
            pass
        assert channel.avatar_image_large.url == channel.avatar_image_large_url
        assert channel.avatar_image_large.width == 88
        assert channel.avatar_image_large.height == 88
        # Original banner_image
        assert channel.banner_image.url
        assert channel.banner_image.width == 1707
        assert channel.banner_image.height == 282
        # Large banner_image
        try:
            channel.banner_image_large.open()
        except ValueError:
            pass
        assert channel.banner_image_large.url == channel.banner_image_large_url
        assert channel.banner_image_large.width == 2560
        assert channel.banner_image_large.height == 1440

    def test_without_images(self, user):
        channel = services.create_channel(
            name='My Channel',
            user=user,
            description='x' * 5000,
            sync_videos_interested=True,
            language='en',
            avatar_image=None,
            banner_image=None,
        )

        assert isinstance(channel, services.models.Channel)
        assert channel.name == 'My Channel'
        assert channel.user == user
        assert channel.description == 'x' * 5000
        assert channel.sync_videos_interested is True
        # Original avatar (default)
        assert not channel.avatar_image
        # Small avatar (default)
        assert not channel.avatar_image_small
        assert channel.avatar_image_small_url.startswith('http://')
        # Large avatar (default)
        assert not channel.avatar_image_large
        assert channel.avatar_image_large_url.startswith('http://')
        # Large banner_image (default)
        assert not channel.banner_image_large
        assert channel.banner_image_large_url.startswith('http://')


class TestGetChannel:
    def test(self, user, channel):
        record = services.get_channel(id=channel.id)

        assert record.id == channel.id
        assert isinstance(record, services.models.Channel)

    def test_with_user_id(self, user, channel):
        record = services.get_channel(id=channel.id, user_id=user.id)

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
