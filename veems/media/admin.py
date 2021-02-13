from django.contrib import admin

from . import models


class VideoRenditionInline(admin.TabularInline):
    model = models.VideoRendition


class TranscodeJobInline(admin.TabularInline):
    model = models.TranscodeJob


class VideoRenditionThumbnailInline(admin.TabularInline):
    model = models.VideoRenditionThumbnail


class VideoAdmin(admin.ModelAdmin):
    inlines = [
        VideoRenditionInline,
        TranscodeJobInline,
    ]

    def get_queryset(self, request):
        return models.Video.objects_all.all()


class VideoRenditionAdmin(admin.ModelAdmin):
    inlines = [
        VideoRenditionThumbnailInline,
    ]


admin.site.register(models.Upload)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.VideoRendition, VideoRenditionAdmin)
admin.site.register(models.TranscodeJob)
admin.site.register(models.VideoLikeDislike)
