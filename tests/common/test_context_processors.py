import pytest

from veems.common import context_processors

pytestmark = pytest.mark.django_db


def test_global_context(rf, user, channel):
    request = rf.get('/?next=/')
    request.user = user

    context = context_processors.global_context(request=request)

    assert isinstance(context, dict)
    assert len(context['channels']) == 1
    assert context['login_form']
    assert context['next'] == '/'
