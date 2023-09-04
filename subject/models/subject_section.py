from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from selection.models import Selection

from .subject import Subject


class SubjectSection(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Subject's section id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    selection = models.ForeignKey(
        verbose_name=_("selection"),
        help_text=_("Selection's id"),
        to=Selection,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    subject = models.ForeignKey(
        verbose_name=_("subject"),
        help_text=_("Subject's id"),
        to=Subject,
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
    taken = models.BooleanField(
        verbose_name=_("taken"),
        help_text=_("Are you going to take this subject?"),
        default=False,
    )

    class Meta:
        verbose_name = _("subject section")
        verbose_name_plural = _("subject sections")
        db_table = "subject_section"

    def __str__(self):
        return f"{self.subject.code}-{self.section}"
