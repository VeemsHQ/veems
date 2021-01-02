from http.client import FOUND, OK
from uuid import uuid4

from django.urls import reverse
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


class TestSignup:
    URL = '/accounts/signup/'

    @pytest.fixture
    def valid_data(self):
        password = '!!password!!TEST'
        return {
            'email': f'{uuid4()}@veems.tv',
            'sync_videos_interested': True,
            'password1': password,
            'password2': password,
        }

    def test_get_returns_html_with_form_in_context(self, client):
        response = client.get(self.URL)

        assert response.status_code == OK
        assert response.context['form']

    def test_post_with_valid_data_creates_new_user(self, client, valid_data):
        response = client.post(self.URL, data=valid_data)

        assert response.status_code == FOUND
        assert response.url == reverse(
            settings.DEFAULT_POST_SIGNUP_REDIRECT_VIEW_NAME
        )
        assert get_user_model().objects.get(
            email=valid_data['email'],
            sync_videos_interested=valid_data['sync_videos_interested'],
        )

    def test_post_with_next_redirects_to_that_url_after_signup(
        self, client, valid_data
    ):
        next_path = reverse('channel-manager-index')
        url = f'{self.URL}?next={next_path}'
        response = client.post(url, data=valid_data)

        assert response.status_code == FOUND
        assert response.url == next_path
        assert get_user_model().objects.get(
            email=valid_data['email'],
            sync_videos_interested=valid_data['sync_videos_interested'],
        )

    def test_post_with_missing_data_returns_errors(self, client, valid_data):
        data = valid_data
        data.pop('password2')

        response = client.post(self.URL, data=data)

        assert response.status_code == OK
        assert response.context['form'].is_valid() is False

    def test_post_with_mismatched_passwords_returns_errors(
        self, client, valid_data
    ):
        data = valid_data
        data['password2'] = 'someThingElse!!1'

        response = client.post(self.URL, data=data)

        assert response.status_code == OK
        assert response.context['form'].is_valid() is False
