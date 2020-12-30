from ..channel import services as channel_services


class GlobalContextMixin:
    def get_context_data(self, *args, **kwargs):
        try:
            context = super().get_context_data(*args, **kwargs)
        except AttributeError:
            context = {}
        context['channels'] = channel_services.get_channels(
            user_id=self.request.user.id
        )
        return context
