from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..stub_data import VIDEOS, CHANNEL_SYNCS


@method_decorator(login_required, name='dispatch')
class LoginRequiredTemplateView(TemplateView):
    pass


class ChannelManagerTemplateView(
    LoginRequiredTemplateView,
):
    pass


class IndexView(ChannelManagerTemplateView):
    template_name = 'channel_manager/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['top_videos'] = VIDEOS[:3]
        return context


class IndexBlankView(ChannelManagerTemplateView):
    template_name = 'channel_manager/index_blank.html'


class VideosView(ChannelManagerTemplateView):
    template_name = 'channel_manager/videos.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['videos'] = VIDEOS[:6]
        return context


class MonetizationView(ChannelManagerTemplateView):
    template_name = 'channel_manager/monetization.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['videos'] = VIDEOS[:6]
        return context


class CustomizationView(ChannelManagerTemplateView):
    template_name = 'channel_manager/customization.html'


class SyncView(ChannelManagerTemplateView):
    template_name = 'channel_manager/sync.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['syncs'] = CHANNEL_SYNCS
        return context


class SyncBlankView(ChannelManagerTemplateView):
    template_name = 'channel_manager/sync-blank.html'
