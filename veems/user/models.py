from django.contrib.auth.models import AbstractUser

from ..common.models import BaseModel


class User(BaseModel, AbstractUser):

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} {self.username}>'
