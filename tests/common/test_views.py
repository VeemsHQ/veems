import pytest

from veems.common import views
from veems.channel import models


pytestmark = pytest.mark.django_db


class TestGlobalContextMixin:
    def test_get_context_data(self, rf, user_factory, channel_factory):
        users = (
            user_factory(),
            user_factory(),
        )
        for user in users:
            channel_factory(user=user)
            channel_factory(user=user)
        request = rf.get('/')
        request.user = users[0]

        context_instance = views.GlobalContextMixin()
        context_instance.request = request
        context = context_instance.get_context_data()

        assert len(context['channels']) == 2
        for channel_record in context['channels']:
            assert isinstance(channel_record, models.Channel)
            assert channel_record.user == request.user
