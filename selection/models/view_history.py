from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .selection import Selection


class ViewHistory(models.Model):
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
        to=Selection,
        on_delete=models.CASCADE,
        related_name="views",
    )
    is_hidden = models.BooleanField(
        verbose_name=_("is hidden"),
        help_text=_("Hidden from history"),
        default=False,
    )
    viewed = models.DateTimeField(
        verbose_name=_("created"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("selection view")
        verbose_name_plural = _("selection views")
        db_table = "selection_view"

    def save(self, *args, **kwargs):
        self.selection.views_count += 1
        self.selection.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.selection.views_count -= 1
        self.selection.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.selection.name} - {self.viewed_by.username}"
