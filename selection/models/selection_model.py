from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class SelectionModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Selection id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    display = models.CharField(
        verbose_name=_("display name"),
        help_text=_("Selection display name"),
        max_length=100,
        default="My Selection",
    )
    name = models.SlugField(
        verbose_name=_("display"),
        help_text=_("Selection display"),
        max_length=100,
        default="My-Selection",
    )
    owner = models.ForeignKey(
        verbose_name=_("owner"),
        help_text=_("Selection's owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="selections",
    )
    is_visible = models.BooleanField(
        verbose_name=_("is visible"),
        help_text=_("Visibility"),
        default=True,
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

        unique_together = ("name", "owner")

    def __str__(self):
        return f"{self.owner.username}/{self.name}"

    def save(self, *args, **kwargs):
        self.name = slugify(self.display)
        return super().save(*args, **kwargs)