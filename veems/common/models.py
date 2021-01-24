from django.db import models

from .fields import ShortUUIDField
from . import managers


class BaseModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(auto_now=True, db_index=True)
    deleted_on = models.DateTimeField(db_index=True, null=True)

    objects = managers.ObjectsManager()
    objects_all = managers.ObjectsAllManager()

    class Meta:
        abstract = True
        ordering = ['created_on']
