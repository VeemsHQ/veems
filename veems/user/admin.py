from django.contrib import admin

from . import models


class UserProfileInline(admin.TabularInline):
    model = models.UserProfile


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
    ]


admin.site.register(models.User, UserAdmin)
