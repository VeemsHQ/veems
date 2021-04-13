from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django_registration.backends.activation.views import (
    RegistrationView,
    ActivationView,
)
import debug_toolbar

from .media import api_views, views as media_views
from .home import views as home_views
from .user import views as user_views, forms as user_forms
from .channel_manager import views as channel_manager_views
from .channel import api_views as channel_api_views, views as channel_views
from .search import views as search_views


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', home_views.IndexView.as_view(), name='index'),
    path(
        'v/<slug:video_id>/',
        media_views.VideoView.as_view(),
        name='view-video',
    ),
    path(
        'c/<slug:channel_id>/',
        channel_views.ChannelIndexView.as_view(),
        name='view-channel',
    ),
    path(
        'results/',
        search_views.SearchView.as_view(),
        name='search',
    ),
    path(
        'c/<slug:channel_id>/about/',
        channel_views.ChannelAboutView.as_view(),
        name='view-channel-about',
    ),
    path(
        'accounts/logout/',
        user_views.logout,
        name='logout',
    ),
    path(
        'accounts/login/',
        user_views.CustomLoginView.as_view(),
        name='login',
    ),
    path(
        'accounts/register/',
        RegistrationView.as_view(
            form_class=user_forms.CustomRegistrationForm,
        ),
        name='django_registration_register',
    ),
    path(
        'accounts/activate/complete/',
        TemplateView.as_view(
            template_name='django_registration/activation_complete.html'
        ),
        name='django_registration_activation_complete',
    ),
    path(
        'accounts/activate/<str:activation_key>/',
        ActivationView.as_view(),
        name='django_registration_activate',
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'channel/',
        channel_manager_views.IndexView.as_view(),
        name='channel-manager-index',
    ),
    path(
        'channel/index-blank',
        channel_manager_views.IndexBlankView.as_view(),
        name='channel-manager-index-blank',
    ),
    path(
        'channel/videos/',
        channel_manager_views.VideosView.as_view(),
        name='channel-manager-videos',
    ),
    path(
        'upload/',
        channel_manager_views.upload_redirect,
        name='upload',
    ),
    path(
        'channel/monetization/',
        channel_manager_views.MonetizationView.as_view(),
        name='channel-manager-monetization',
    ),
    path(
        'channel/customization/',
        channel_manager_views.CustomizationView.as_view(),
        name='channel-manager-customization',
    ),
    path(
        'channel/sync/',
        channel_manager_views.SyncView.as_view(),
        name='channel-manager-sync',
    ),
    path(
        'channel/sync-blank/',
        channel_manager_views.SyncBlankView.as_view(),
        name='channel-manager-sync-blank',
    ),
    path('api/v1/channel/', channel_api_views.ChannelAPIView.as_view()),
    path(
        'api/v1/channel/<slug:channel_id>/',
        channel_api_views.ChannelDetailAPIView.as_view(),
    ),
    path(
        'api/v1/channel/<slug:channel_id>/avatar/',
        channel_api_views.ChannelAvatarAPIView.as_view(),
    ),
    path(
        'api/v1/channel/<slug:channel_id>/banner/',
        channel_api_views.ChannelBannerAPIView.as_view(),
    ),
    path('api/v1/upload/prepare/', api_views.upload_prepare),
    path('api/v1/upload/<slug:upload_id>/', api_views.upload_detail),
    path(
        'api/v1/upload/complete/<slug:upload_id>/', api_views.upload_complete
    ),
    path('api/v1/video/', api_views.VideoAPIView.as_view()),
    path(
        'api/v1/video/<slug:video_id>/', api_views.VideoDetailAPIView.as_view()
    ),
    path(
        'api/v1/video/<slug:video_id>/likedislike/',
        api_views.VideoLikeDislikeAPIView.as_view(),
    ),
    path(
        'api/v1/video/<slug:video_id>/thumbnail/',
        api_views.VideoThumbnailAPIView.as_view(),
    ),
    path(
        'api/v1/video/<slug:video_id>/thumbnail/'
        '<slug:video_rendition_thumbnail_id>/',
        api_views.VideoThumbnailSelectAPIView.as_view(),
    ),
    path(
        'api/v1/video/<slug:video_id>/playlist.m3u8',
        api_views.video_playlist,
        name='api-video-playlist',
    ),
]
