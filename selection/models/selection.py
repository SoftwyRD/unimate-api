from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Selection(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Selection id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Selection name"),
        max_length=100,
        default="My Selection",
    )
    owner = models.ForeignKey(
        verbose_name=_("owner"),
        help_text=_("Selection's owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="selections",
    )
    views_count = models.IntegerField(
        verbose_name=_("views count"),
        help_text=_("Views count"),
        validators=[MinValueValidator(0)],
        default=0,
    )
    stars_count = models.IntegerField(
        verbose_name=_("stars count"),
        help_text=_("Stars count"),
        validators=[MinValueValidator(0)],
        default=0,
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
        verbose_name = _("selection")
        verbose_name_plural = _("selections")
        db_table = "selection"

    def __str__(self):
        return self.name
