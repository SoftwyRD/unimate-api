from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models


class Subject(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=255, unique=True)
    credits = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_lab = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """Save the subject with the code in uppercase."""
        self.code = self.code.upper()
        super().save(*args, **kwargs)
