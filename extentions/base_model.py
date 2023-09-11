from django.db import models
from django.db.models import Model as DjangoModel


class BaseModel(DjangoModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
