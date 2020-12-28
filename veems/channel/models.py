from django.db import models
from django.contrib.auth import get_user_model

from ..common.models import BaseModel
from ..common import validators


class Channel(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=5000)
    sync_videos_interested = models.BooleanField(null=False)
    language = models.CharField(
        max_length=2, validators=(validators.validate_language,),
        null=False, blank=False, default=None,
    )
