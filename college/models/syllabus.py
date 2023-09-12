from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .career import Career

from datetime import datetime


class Syllabus(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Syllabus id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    career = models.ForeignKey(
        verbose_name=_("career"),
        help_text=_("Career"),
        to=Career,
        on_delete=models.CASCADE,
        related_name="syllabuses",
    )
    year = models.IntegerField(
        verbose_name=_("year"),
        help_text=_("Syllabus year"),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 5),
        ],
        default=datetime.now().year,
    )
    version = models.CharField(
        verbose_name=_("version"),
        help_text=_("Syllabus version"),
        max_length=30,
        null=True,
        blank=True,
    )
    credits = models.IntegerField(
        verbose_name=_("credits"),
        help_text=_("Credits"),
        validators=[MinValueValidator(0)],
        default=0,
    )
    subjects_count = models.IntegerField(
        verbose_name=_("subjects"),
        help_text=_("Subjects count"),
        validators=[MinValueValidator(0)],
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        help_text=_("is syllabus active"),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name=_("modified at"),
        help_text=_("Last modification date"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("syllabus")
        verbose_name_plural = _("syllabuses")
        db_table = "syllabus"

    def __str__(self):
        return (
            f"{self.career.name} ({self.year}) - "
            + f"{self.career.college.full_name}"
        )
