from django.contrib.auth import get_user_model
import pytest

from veems.common.management.commands import import_seed_data
from veems.channel import services as channel_services
from veems.media.models import Video

pytestmark = pytest.mark.django_db


def test_run():
    import_seed_data._run()

    assert get_user_model().objects.filter(is_superuser=True).count() == 2
    assert len(channel_services.get_channels()) == 3
    assert Video.objects.count() == 1
