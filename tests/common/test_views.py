from veems.common import views


class TestGlobalContextMixin:
    def test_get_context_data(self):
        context = views.GlobalContextMixin().get_context_data()

        assert context['channels']
        assert isinstance(context['channels'], tuple)
