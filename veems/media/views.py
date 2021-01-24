from django.views.generic import TemplateView

from . import services, serializers
from ..channel import serializers as channel_serializers


class VideoView(TemplateView):
    template_name = 'media/video.html'

    def get_context_data(self, *args, video_id, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        video = services.get_video(id=video_id)
        video_data = serializers.VideoSerializer(
            instance=video, user_id=self.request.user.id
        ).data
        context['video'] = video_data
        channel_data = channel_serializers.ChannelSlimSerializer(
            instance=video.channel
        ).data
        context['channel'] = channel_data
        return context
