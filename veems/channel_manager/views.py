from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..stub_data import VIDEOS, CHANNEL_SYNCS


@method_decorator(login_required, name='dispatch')
class LoginRequiredTemplateView(TemplateView):
    pass


class IndexView(LoginRequiredTemplateView):
    template_name = 'channel_manager/index.html'

    def get_context_data(self):
        data = {'top_videos': VIDEOS[:3]}
        return data


class IndexBlankView(LoginRequiredTemplateView):
    template_name = 'channel_manager/index_blank.html'


class VideosView(LoginRequiredTemplateView):
    template_name = 'channel_manager/videos.html'

    def get_context_data(self):
        data = {'videos': VIDEOS[:6]}
        return data


class MonetizationView(LoginRequiredTemplateView):
    template_name = 'channel_manager/monetization.html'

    def get_context_data(self):
        data = {'videos': VIDEOS[:5]}
        return data


class CustomizationView(LoginRequiredTemplateView):
    template_name = 'channel_manager/customization.html'


class SyncView(LoginRequiredTemplateView):
    template_name = 'channel_manager/sync.html'

    def get_context_data(self):
        data = {'syncs': CHANNEL_SYNCS}
        return data


class SyncBlankView(LoginRequiredTemplateView):
    template_name = 'channel_manager/sync-blank.html'
