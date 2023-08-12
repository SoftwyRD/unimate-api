from django.core.validators import MinValueValidator
from django.db import models
from selection.models import Selection
from subject.models import Subject


class SubjectSection(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    section = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    professor = models.CharField(max_length=60)
    taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject.code}-{self.section}"
