from http.client import OK

import pytest

pytestmark = pytest.mark.django_db


class TestSearchView:
    @pytest.fixture(autouse=True)
    def setup_method(self, channel_factory, user, video_factory, channel):
        channel_factory(name='Cheese', user=user)
        channel_factory(name='Pizza Recipes', description='Cheese', user=user)
        channel_factory(name='Cheese on Toast recipes', user=user)
        channel_factory(name='Carrot', description='Cheesy', user=user)
        video_factory(
            channel=channel, title='I love cheese cake', visibility='public'
        )
        video_factory(
            channel=channel,
            title='I love cheese cake also',
            visibility='private',
        )

    @pytest.mark.parametrize('query_type', ['', 'videos', 'channels'])
    def test(self, client, query_type):
        response = client.get(
            f'/results/?search_query=cheese&query_type={query_type}'
        )

        assert response.status_code == OK
        assert response.context['search_query'] == 'cheese'
        assert response.context['query_type'] == query_type or 'videos'
        assert len(response.context['video_results']) == 1
        assert len(response.context['channel_results']) == 3
