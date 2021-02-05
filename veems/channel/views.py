from django.views.generic import TemplateView

from ..media import (
    serializers as media_serializers,
    services as media_services,
)
from . import services, serializers


class ChannelContextMixin:
    def get_context_data(
        self, *args, channel_id, include_videos=False, **kwargs
    ):
        context = super().get_context_data(
            *args, channel_id=channel_id, **kwargs
        )
        if include_videos:
            videos = media_services.get_videos(channel_id=channel_id)
            videos_data = media_serializers.VideoSummarySerializer(
                videos, many=True
            ).data
            context['channel_videos'] = videos_data
        channel = services.get_channel(id=channel_id)
        channel_data = serializers.ChannelSummarySerializer(
            instance=channel
        ).data
        context['channel'] = channel_data
        context['is_owner'] = channel_data['user'] == self.request.user.id
        return context


class ChannelIndexView(ChannelContextMixin, TemplateView):
    template_name = 'channel/index.html'

    def get_context_data(self, *args, channel_id, **kwargs):
        return super().get_context_data(
            *args, channel_id=channel_id, include_videos=True, **kwargs
        )


class ChannelAboutView(ChannelContextMixin, TemplateView):
    template_name = 'channel/about.html'
