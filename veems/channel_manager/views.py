from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..stub_data import VIDEOS, CHANNEL_SYNCS
from ..channel import services as channel_services
from ..media import (
    services as media_services,
    serializers as media_serializers,
)
from . import forms


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
        channel_videos = media_services.get_videos(
            channel_id=channel_id,
            user_id=self.request.user.id,
        )
        channel_videos = media_serializers.VideoSerializer(
            instance=channel_videos, many=True
        ).data
        channel_uploads_processing = media_services.get_uploads_processing(
            channel_id=channel_id,
            user_id=self.request.user.id,
        )
        channel_uploads_processing = media_serializers.UploadSummarySerializer(
            instance=channel_uploads_processing, many=True
        ).data
        context['channel_videos'] = channel_videos
        context['channel_uploads_processing'] = channel_uploads_processing
        context['channel_id'] = channel_id
        return context


def upload_redirect(request):
    return redirect(
        reverse('channel-manager-videos') + '?display=upload-modal'
    )


class MonetizationView(ChannelManagerTemplateView):
    template_name = 'channel_manager/coming-soon-monetization.html'


class CustomizationView(ChannelManagerTemplateView):
    template_name = 'channel_manager/customization.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        channel = channel_services.get_selected_channel(user=self.request.user)
        context['channel'] = channel
        # TODO: test
        context['reload_page_after_channel_selected'] = True
        context['channel_basic_info_saved'] = False
        context['channel_avatar_image_saved'] = False
        context['channel_banner_image_saved'] = False
        context['errors'] = None
        return context

    def post(self, request):
        channel = channel_services.get_selected_channel(user=self.request.user)
        form = forms.ChannelForm(
            instance=channel, data=request.POST, files=request.FILES
        )
        context = self.get_context_data()
        if form.is_valid():
            field_updates = {k: v for k, v in form.cleaned_data.items() if v}
            channel_services.update_channel(
                channel=form.instance, **field_updates
            )
            if form.cleaned_data['name'] or form.cleaned_data['description']:
                context['channel_basic_info_saved'] = True
            if isinstance(
                form.cleaned_data['avatar_image'], InMemoryUploadedFile
            ):
                context['channel_avatar_image_saved'] = True
            if isinstance(
                form.cleaned_data['banner_image'], InMemoryUploadedFile
            ):
                context['channel_banner_image_saved'] = True
        else:
            context['errors'] = form.errors
        return render(
            request=request, template_name=self.template_name, context=context
        )


class SyncView(ChannelManagerTemplateView):
    template_name = 'channel_manager/sync.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['syncs'] = CHANNEL_SYNCS
        return context


class SyncBlankView(ChannelManagerTemplateView):
    template_name = 'channel_manager/sync-blank.html'
