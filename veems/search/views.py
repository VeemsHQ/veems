from django.views.generic import TemplateView

from ..media import (
    serializers as media_serializers,
    services as media_services,
)
from ..channel import (
    services as channel_services, serializers as channel_serializers
)


class SearchView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self, *args, query, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query_type = self.request.GET.get('type', '').lower()
        context['video_results'] = []
        context['channel_results'] = []
        if not query_type or query_type == 'videos':
            videos = media_services.get_popular_videos()
            videos = media_serializers.VideoSlimSerializer(
                videos, many=True
            ).data
            context['video_results'] = videos
        elif query_type == 'channels':
            channels = channel_services.get_channels()
            channels = channel_serializers.ChannelSlimSerializer(
                channels, many=True
            ).data
            context['channel_results'] = channels
        context['search_query'] = query
        return context
