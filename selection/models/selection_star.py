from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .selection import Selection


class SelectionStar(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Selection star id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    selection = models.ForeignKey(
        verbose_name=_("selection"),
        help_text=_("Starred selection"),
        to=Selection,
        on_delete=models.CASCADE,
        related_name="stars",
    )
    starred_by = models.ForeignKey(
        verbose_name=_("starred by"),
        help_text=_("Starred by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="starred_selections",
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("selection star")
        verbose_name_plural = _("selection stars")
        db_table = "selection_star"

        unique_together = ("selection", "starred_by")

    def save(self, *args, **kwargs):
        self.selection.stars_count += 1
        self.selection.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.selection.stars_count -= 1
        self.selection.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.selection.name} - {self.starred_by.username}"
