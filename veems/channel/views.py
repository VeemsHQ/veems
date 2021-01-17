from django.views.generic import TemplateView

from ..media import (
    serializers as media_serializers,
    services as media_services,
)
from . import services, serializers


def _get_context_data(*, context, channel_id, request, include_videos=False):
    if include_videos:
        videos = media_services.get_videos(channel_id=channel_id)
        videos_data = media_serializers.VideoSlimSerializer(
            videos, many=True
        ).data
        context['channel_videos'] = videos_data
    channel = services.get_channel(id=channel_id)
    channel_data = serializers.ChannelSlimSerializer(channel).data
    context['channel'] = channel_data
    context['is_owner'] = channel_data['user'] == request.user.id
    return context


class ChannelIndexView(TemplateView):
    template_name = 'channel/index.html'

    def get_context_data(self, *args, channel_id, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return _get_context_data(
            context=context,
            channel_id=channel_id,
            request=self.request,
            include_videos=True,
        )


class ChannelAboutView(TemplateView):
    template_name = 'channel/about.html'

    def get_context_data(self, *args, channel_id, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return _get_context_data(
            context=context, channel_id=channel_id, request=self.request
        )
