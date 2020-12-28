from uuid import uuid4
import pytest
from django.contrib.auth import get_user_model

from veems.channel import services


@pytest.fixture
def user_factory():
    def make():
        user = get_user_model().objects.create(
            username=f'user{str(uuid4())[:5]}',
        )
        user.set_password(f'password{str(uuid4())}')
        return user

    return make


@pytest.fixture
def user(user_factory):
    return user_factory()


@pytest.fixture
def channel(user):
    return services.create_channel(
        name='My Channel',
        user=user,
        description='x' * 5000,
        sync_videos_interested=True,
        language='en',
    )
