import pytest
from django.contrib.auth import get_user_model

from veems.user import models

pytestmark = pytest.mark.django_db


def test_profile_is_created_when_user_created():
    user = get_user_model().objects.create(
        username='1@example.com',
        email='1@example.com',
    )

    assert user.profile
    assert isinstance(user.profile, models.UserProfile)
    assert user.profile.sync_videos_interested is False
