import pytest

from veems.user import forms

pytestmark = pytest.mark.django_db


class TestCustomRegistrationForm:
    @pytest.mark.parametrize('sync_videos_interested', [True, False])
    def test(self, sync_videos_interested):
        data = {
            'email': '1@example.com',
            'password1': 'dASDFA£RFF!!!',
            'password2': 'dASDFA£RFF!!!',
            'sync_videos_interested': (
                'on' if sync_videos_interested else 'off'
            ),
        }
        if not sync_videos_interested:
            del data['sync_videos_interested']

        form = forms.CustomRegistrationForm(data=data)
        assert form.is_valid()
        user = form.save()

        assert user.email == '1@example.com'
        assert user.password
        assert user.profile.sync_videos_interested == sync_videos_interested
