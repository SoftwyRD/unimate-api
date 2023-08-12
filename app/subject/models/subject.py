from django.core.validators import MinValueValidator
from django.db import models


class Subject(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=255, unique=True)
    credits = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)
