from django.contrib.auth.models import BaseUserManager


from ..common import managers


class UserObjectsManager(managers.ObjectsManager, BaseUserManager):
    pass


class UserObjectsAllManager(managers.ObjectsAllManager, BaseUserManager):
    pass
