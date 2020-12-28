from ..stub_data import CHANNELS


class GlobalContextMixin:
    def get_context_data(self, *args, **kwargs):
        try:
            context = super().get_context_data(*args, **kwargs)
        except AttributeError:
            context = {}
        context['channels'] = CHANNELS
        return context
