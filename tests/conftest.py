from uuid import uuid4
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from veems.channel import services


TEST_DATA_DIR = Path(__file__).parent / 'test_data'
EXAMPLE_IMG = TEST_DATA_DIR / 'example-image.jpeg'


@pytest.fixture
def simple_uploaded_img_file():
    with EXAMPLE_IMG.open('rb') as file_:
        file_contents = file_.read()
    return SimpleUploadedFile(EXAMPLE_IMG.name, file_contents)


@pytest.fixture
def simple_uploaded_img_file_factory():
    def make(path=EXAMPLE_IMG):
        with path.open('rb') as file_:
            file_contents = file_.read()
        return SimpleUploadedFile(path.name, file_contents)
    return make


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
    def make(*, user, avatar_image=None, banner_image=None, is_selected=True):
        return services.create_channel(
            name='My Channel',
            user=user,
            description='x' * 5000,
            sync_videos_interested=True,
            language='en',
            avatar_image=avatar_image,
            banner_image=banner_image,
            is_selected=is_selected,
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
