from django.db import models


class ObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_on__isnull=True)


class ObjectsAllManager(models.Manager):
    pass
