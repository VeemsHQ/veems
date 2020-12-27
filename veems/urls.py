from django.contrib import admin
from django.urls import path

from .media import api_views
from .home import views as home_views
from .channel_manager import views as channel_manager_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.IndexView.as_view(), name='index'),
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
    path('api/v1/upload/prepare/', api_views.upload_prepare),
    path(
        'api/v1/upload/complete/<slug:upload_id>/', api_views.upload_complete
    ),
    path('api/v1/video/<slug:video_id>/', api_views.video),
    path(
        'api/v1/video/<slug:video_id>/playlist.m3u8',
        api_views.video_playlist,
        name='api-video-playlist',
    ),
]
