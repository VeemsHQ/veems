from django.views.generic import TemplateView

from ..media import (
    serializers as media_serializers,
    services as media_services,
)


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        videos_popular = media_services.get_popular_videos()
        videos_popular = media_serializers.VideoSlimSerializer(
            videos_popular, many=True
        ).data
        context['videos_popular'] = videos_popular
        return context
