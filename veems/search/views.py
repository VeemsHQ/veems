from django.views.generic import TemplateView

from ..media import serializers as media_serializers
from ..channel import serializers as channel_serializers
from ..search import services


class SearchView(TemplateView):
    template_name = 'search/index.html'

    def get_context_data(self, *args, query, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query_type = self.request.GET.get('type', '').lower()
        search_results = services.search(query=query, query_type=query_type)
        context['video_results'] = media_serializers.VideoSlimSerializer(
            search_results['videos'], many=True
        ).data
        context['channel_results'] = channel_serializers.ChannelSlimSerializer(
            search_results['channels'], many=True
        ).data

        context['search_query'] = query
        return context
