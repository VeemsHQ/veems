from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..common.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField(_('email address'), null=False, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        null=True, blank=True,
    )
    sync_videos_interested = models.BooleanField(null=False, default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} {self.email}>'
