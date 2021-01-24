from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
import logging

from django.utils.translation import gettext_lazy as _

from ..common.models import BaseModel
from . import managers

logger = logging.getLogger(__name__)


class User(BaseModel, AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        null=True,
        blank=True,
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = managers.UserObjectsManager()
    objects_all = managers.UserObjectsAllManager()

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} {self.email}>'


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE
    )
    sync_videos_interested = models.BooleanField(default=False)


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info('Creating User Profile for %s', instance)
        return UserProfile.objects.create(user=instance)
