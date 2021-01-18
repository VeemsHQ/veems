from django.views.generic import TemplateView

from ..media import (
    serializers as media_serializers,
    services as media_services,
)


class SearchView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self, *args, query, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        videos = media_services.get_popular_videos()
        videos = media_serializers.VideoSlimSerializer(
            videos, many=True
        ).data
        context['video_results'] = videos
        context['channel_results'] = []
        context['search_query'] = query
        return context
