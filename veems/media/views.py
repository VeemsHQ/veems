from django.views.generic import TemplateView
from django.urls import reverse

from . import services


class VideoView(TemplateView):
    template_name = 'media/play_video.html'

    def get_context_data(self, *args, video_id, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        video = services.get_video(id=video_id)
        context['video_rendition_count'] = video.videorendition_set.count()
        context['video_id'] = video.id
        context['video_title'] = video.title
        context['video_description'] = video.description
        context['video_view_count'] = 0
        context['video_comment_count'] = 0
        context['video_created_date'] = video.created_on.date()
        context['video_playlist_url'] = reverse(
            'api-video-playlist', args=[video.id]
        )
        channel = video.channel
        context['channel_followers_count'] = 0
        context['channel_name'] = channel.name
        context['channel_id'] = channel.id
        context['channel_description'] = channel.description
        context['channel_avatar_image_small_url'] = (
            channel.avatar_image_small_url
        )
        context['channel_banner_image_small_url'] = (
            channel.banner_image_small_url
        )
        return context
