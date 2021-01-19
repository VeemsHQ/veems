from django.views.generic import TemplateView

from ..media import serializers as media_serializers
from ..channel import serializers as channel_serializers
from ..search import services


class SearchView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_query = self.request.GET['search_query']
        query_type = self.request.GET.get('type', '').lower() or 'videos'
        search_results = services.search(query=search_query)
        context['video_results'] = media_serializers.VideoSlimSerializer(
            search_results['videos'], many=True
        ).data
        context['channel_results'] = channel_serializers.ChannelSlimSerializer(
            search_results['channels'], many=True
        ).data
        context['search_query'] = search_query
        context['query_type'] = query_type
        return context
