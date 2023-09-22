from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from subject.models import SubjectModel

from .syllabus_model import SyllabusModel


class SyllabusSubjectModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Syllabus subject id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    syllabus = models.ForeignKey(
        verbose_name=_("syllabus"),
        help_text=_("Syllabus"),
        to=SyllabusModel,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    subject = models.ForeignKey(
        verbose_name=_("subject"),
        help_text=_("Syllabus' subject"),
        to=SubjectModel,
        on_delete=models.CASCADE,
        related_name="syllabuses",
    )
    cycle = models.IntegerField(
        verbose_name=_("cycle"),
        help_text=_("Cycle on syllabus"),
        validators=[MinValueValidator(0)],
        default=1,
    )

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        db_table = "syllabus_subject"

        unique_together = ("syllabus", "subject")

    def __str__(self):
        return (
            f"{self.syllabus.career.name} ({self.syllabus.version}) - "
            + f"{self.syllabus.career.college.name} | {self.subject}"
        )
