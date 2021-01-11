import pytest
from django.contrib.auth.models import AnonymousUser

from veems.common import context_processors

pytestmark = pytest.mark.django_db


class TestGlobalContext:
    def test(self, rf, user, channel):
        request = rf.get('/?next=/')
        request.user = user

        context = context_processors.global_context(request=request)

        assert isinstance(context, dict)
        assert len(context['channels']) == 1
        assert context['login_form']
        assert context['next'] == '/'
        assert context['selected_channel'] == channel.id

    def test_user_without_any_channels(self, rf, user):
        request = rf.get('/?next=/')
        request.user = user

        context = context_processors.global_context(request=request)

        assert isinstance(context, dict)
        assert len(context['channels']) == 0
        assert context['login_form']
        assert context['next'] == '/'
        assert context['selected_channel'] is None

    def test_unauthenticated(self, rf, user, channel):
        request = rf.get('/?next=/')
        request.user = AnonymousUser()

        context = context_processors.global_context(request=request)

        assert isinstance(context, dict)
        assert context['channels'] == []
        assert context['login_form']
        assert context['next'] == '/'
        assert context['selected_channel'] is None
