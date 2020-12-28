from django.db import models
from django.contrib.auth import get_user_model

from ..common.models import BaseModel

VISIBILITY_CHOICES = (
    'private',
    'public',
    'unlisted',
)


class Channel(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=5000)
    visibility = models.CharField(
        max_length=10,
        choices=tuple((c, c) for c in VISIBILITY_CHOICES),
    )
