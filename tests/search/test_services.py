import pytest


from veems.search import services

pytestmark = pytest.mark.django_db


class TestSearch:
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

    def test(self):
        results = services.search(query='cheese')

        channel_results = results['channels']
        assert len(channel_results) == 3
        names = sorted((r.name for r in channel_results))
        assert names == sorted(
            ('Cheese', 'Cheese on Toast recipes', 'Pizza Recipes')
        )

        video_results = results['videos']
        assert len(video_results) == 1

    def test_limit(self):
        results = services.search(query='cheese', limit=2)

        channel_results = results['channels']
        assert len(channel_results) == 2
        names = sorted((r.name for r in channel_results))
        assert names == sorted(('Cheese', 'Cheese on Toast recipes'))

        video_results = results['videos']
        assert len(video_results) == 1
