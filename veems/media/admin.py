from django.contrib import admin

from . import models


class VideoRenditionInline(admin.TabularInline):
    model = models.VideoRendition


class VideoAdmin(admin.ModelAdmin):
    inlines = [
        VideoRenditionInline,
    ]


admin.site.register(models.Upload)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.VideoRendition)
admin.site.register(models.TranscodeJob)
