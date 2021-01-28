from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..stub_data import VIDEOS, CHANNEL_SYNCS
from ..channel import services as channel_services
from ..media import (
    services as media_services,
    serializers as media_serializers,
)


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
        channel_id = channel_services.get_selected_channel_id(
            user=self.request.user
        )
        channel_videos = media_services.get_videos(channel_id=channel_id)
        channel_videos = media_serializers.VideoSerializer(
            instance=channel_videos, many=True
        ).data
        context['channel_videos'] = channel_videos
        return context


class MonetizationView(ChannelManagerTemplateView):
    template_name = 'channel_manager/coming-soon-monetization.html'


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
