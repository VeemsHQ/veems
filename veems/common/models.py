from django.db import models

from .fields import ShortUUIDField


class BaseModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['created_on']
