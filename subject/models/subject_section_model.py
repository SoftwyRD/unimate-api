from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .subject_model import SubjectModel


class SubjectSectionModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Subject's section id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    subject = models.ForeignKey(
        verbose_name=_("subject"),
        help_text=_("Subject's id"),
        to=SubjectModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sections",
    )
    section = models.IntegerField(
        verbose_name=_("section"),
        help_text=_("Subject's section"),
        default=1,
        validators=[MinValueValidator(0)],
    )
    professor = models.CharField(
        verbose_name=_("professor"),
        help_text=_("Professor's name"),
        max_length=60,
    )
    is_custom = models.CharField(
        verbose_name=_("is custom"),
        help_text=_("is section"),
        max_length=60,
    )
    cycle = models.IntegerField(
        verbose_name=_("cycle"),
        help_text=_("cycle"),
        validators=[MinValueValidator(1)],
        default=1,
    )
    year = models.IntegerField(
        verbose_name=_("year"),
        help_text=_("year"),
        validators=[MinValueValidator(1900)],
        default=datetime.now().year,
    )

    class Meta:
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        db_table = "subject_section"

    def __str__(self):
        return (
            f"{self.subject.code}-{self.section} - {self.subject.name}"
            + f" | {self.subject.college.name}"
        )
