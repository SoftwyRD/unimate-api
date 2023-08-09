from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from selection.models import SubjectSection, Weekday


class SectionSchedule(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    section = models.ForeignKey(
        SubjectSection,
        on_delete=models.CASCADE,
        related_name="subject_schedule",
    )
    weekday = models.ForeignKey(Weekday, on_delete=models.SET_NULL, null=True)
    start_time = models.IntegerField(
        default=7, validators=[MinValueValidator(7), MaxValueValidator(20)]
    )
    end_time = models.IntegerField(
        default=9, validators=[MinValueValidator(9), MaxValueValidator(22)]
    )

    def __str__(self) -> str:
        return str(self.id)
