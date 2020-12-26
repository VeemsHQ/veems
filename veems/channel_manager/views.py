from django.views.generic import TemplateView

from ..stub_data import VIDEOS, CHANNEL_SYNCS


class IndexView(TemplateView):
    template_name = 'channel_manager/index.html'

    def get_context_data(self):
        data = {'top_videos': VIDEOS[:3]}
        return data


class IndexBlankView(TemplateView):
    template_name = 'channel_manager/index_blank.html'


class VideosView(TemplateView):
    template_name = 'channel_manager/videos.html'

    def get_context_data(self):
        data = {'videos': VIDEOS[:6]}
        return data


class MonetizationView(TemplateView):
    template_name = 'channel_manager/monetization.html'

    def get_context_data(self):
        data = {'videos': VIDEOS[:5]}
        return data


class CustomizationView(TemplateView):
    template_name = 'channel_manager/customization.html'


class SyncView(TemplateView):
    template_name = 'channel_manager/sync.html'

    def get_context_data(self):
        data = {'syncs': CHANNEL_SYNCS}
        return data


class SyncBlankView(TemplateView):
    template_name = 'channel_manager/sync-blank.html'
