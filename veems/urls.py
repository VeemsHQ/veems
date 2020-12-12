from django.contrib import admin
from django.urls import path

from .media import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/upload/prepare/', api_views.upload_prepare),
    path(
        'api/v1/upload/complete/<slug:upload_id>/', api_views.upload_complete
    ),
    path('api/v1/video/<slug:video_id>/', api_views.video),
]
