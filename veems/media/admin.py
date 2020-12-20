from django.contrib import admin

from . import models

admin.site.register(models.Upload)
admin.site.register(models.Video)
admin.site.register(models.MediaFile)
admin.site.register(models.TranscodeJob)
