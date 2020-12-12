from django.contrib.auth.models import AbstractUser

from ..common.models import BaseModel


class User(BaseModel, AbstractUser):
    pass
