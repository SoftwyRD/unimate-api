from django.db import models


class Weekday(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
