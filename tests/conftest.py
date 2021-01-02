from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from veems.channel import services


@pytest.fixture
def user_factory():
    def make():
        unique = f'user{str(uuid4())[:5]}'
        email = f'{unique}@veems.tv'
        user = get_user_model().objects.create(
            username=email,
            email=email,
        )
        user.set_password(f'password{str(uuid4())}')
        return user

    return make


@pytest.fixture
def user(user_factory):
    return user_factory()


@pytest.fixture
def channel_factory():
    def make(*, user):
        return services.create_channel(
            name='My Channel',
            user=user,
            description='x' * 5000,
            sync_videos_interested=True,
            language='en',
        )

    return make


@pytest.fixture
def channel(user, channel_factory):
    return channel_factory(user=user)


@pytest.fixture
def api_client(user_factory):
    user = user_factory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def api_client_factory(user_factory):
    def make():
        user = user_factory()
        client = APIClient()
        client.force_authenticate(user=user)
        return client, user

    return make


@pytest.fixture
def api_client_no_auth():
    return APIClient()
