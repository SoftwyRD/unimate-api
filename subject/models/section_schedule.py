from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .subject_section import SubjectSection
from .weekday import Weekday


class SectionSchedule(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Section's schedule id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    section = models.ForeignKey(
        verbose_name=_("section"),
        help_text=_("Section's id"),
        to=SubjectSection,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    weekday = models.ForeignKey(
        verbose_name=_("weekday"),
        help_text=_("Weekday id"),
        to=Weekday,
        on_delete=models.PROTECT,
        null=True,
        related_name="weekdays",
    )
    start_time = models.IntegerField(
        verbose_name=_("start time"),
        help_text=_("Section's start time"),
        default=6,
        validators=[MinValueValidator(6), MaxValueValidator(20)],
    )
    end_time = models.IntegerField(
        verbose_name=_("end time"),
        help_text=_("Section's end time"),
        default=8,
        validators=[MinValueValidator(8), MaxValueValidator(22)],
    )

    class Meta:
        verbose_name = _("section schedule")
        verbose_name_plural = _("section schedules")
        db_table = "section_schedule"

    def __str__(self):
        return str(self.id)
