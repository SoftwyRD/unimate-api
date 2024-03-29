from django.db import models
from django.utils.translation import gettext_lazy as _

from selection.models import SelectionModel

from .subject_section_model import SubjectSectionModel


class SelectedSectionModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Selected section id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    selection = models.ForeignKey(
        verbose_name=_("selection"),
        help_text=_("Selected selection"),
        to=SelectionModel,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    section = models.ForeignKey(
        verbose_name=_("section"),
        help_text=_("Section"),
        to=SubjectSectionModel,
        on_delete=models.CASCADE,
        related_name="selections",
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        help_text=_("Is active on selection"),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("selected section")
        verbose_name_plural = _("selected sections")
        db_table = "selected_section"

    def __str__(self):
        return f"{self.selection} - {self.section}"
