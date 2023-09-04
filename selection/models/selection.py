from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Selection(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("Selection id"),
        primary_key=True,
        default=uuid4,
        unique=True,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Selection name"),
        max_length=100,
        default="My Selection",
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        help_text=_("Selection's owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="selections",
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_("modified"),
        help_text=_("Last modification date"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("selection")
        verbose_name_plural = _("selections")
        db_table = "selection"

    def __str__(self):
        return self.name
