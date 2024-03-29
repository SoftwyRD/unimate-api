from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .selection_model import SelectionModel


class ViewHistoryModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Selection view id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    viewed_by = models.ForeignKey(
        verbose_name=_("viewed by"),
        help_text=_("Viewed by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="viewed_selections",
    )
    selection = models.ForeignKey(
        verbose_name=_("selection"),
        help_text=_("Viewed selection"),
        to=SelectionModel,
        on_delete=models.CASCADE,
        related_name="views",
    )
    viewed_at = models.DateTimeField(
        verbose_name=_("viewed at"),
        help_text=_("Viewed at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("selection view")
        verbose_name_plural = _("selection views")
        db_table = "selection_view"

    def __str__(self):
        return f"{self.selection.name} - {self.viewed_by.username}"
