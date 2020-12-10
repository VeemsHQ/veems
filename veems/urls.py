from django.contrib import admin
from django.urls import path

from .media import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/upload/prepare/', views.upload_prepare),
    path('api/v1/upload/complete/<slug:upload_id>/', views.upload_complete),
]
