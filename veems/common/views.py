from ..stub_data import CHANNELS


class GlobalContextMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['channels'] = CHANNELS
        return context
