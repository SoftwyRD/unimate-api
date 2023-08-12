from uuid import uuid4

from django.conf import settings
from django.db import models


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
