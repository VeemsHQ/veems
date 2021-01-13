import pytest

pytestmark = pytest.mark.django_db


class TestChannel:
    def test_avatar_image_url(
        self, channel_factory, user, simple_uploaded_img_file
    ):
        channel = channel_factory(
            user=user, avatar_image=simple_uploaded_img_file
        )

        assert channel.avatar_image_url
        assert channel.avatar_image_url == channel.avatar_image.url

    def test_avatar_image_url_returns_default_when_not_set(
        self,
        channel_factory,
        user,
    ):
        channel = channel_factory(user=user, avatar_image=None)

        assert not channel.avatar_image
        assert channel.avatar_image_url
        assert 'defaults/avatar.svg' in channel.avatar_image_url

    def test_banner_image_large_url(
        self, channel_factory, user, simple_uploaded_img_file
    ):
        channel = channel_factory(
            user=user, banner_image=simple_uploaded_img_file
        )

        assert channel.banner_image_large_url
        assert 'defaults/' not in channel.banner_image_large_url

    def test_banner_image_small_url(
        self, channel_factory, user, simple_uploaded_img_file
    ):
        channel = channel_factory(
            user=user, banner_image=simple_uploaded_img_file
        )

        assert channel.banner_image_small_url
        assert 'defaults/' not in channel.banner_image_small_url

    def test_banner_image_large_url_returns_default_when_not_set(
        self,
        channel_factory,
        user,
    ):
        channel = channel_factory(user=user, banner_image=None)

        assert not channel.banner_image
        assert channel.banner_image_large_url
        assert (
            'defaults/channel-banner-image.png'
            in channel.banner_image_large_url
        )
