from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CollegeModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("College id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("College's name"),
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(
        verbose_name=_("full name"),
        help_text=_("College's full name"),
        max_length=50,
        unique=True,
    )
    careers_count = models.IntegerField(
        verbose_name=_("careers"),
        help_text=_("Careers count"),
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
        verbose_name = _("college")
        verbose_name_plural = _("colleges")
        db_table = "college"

    def __str__(self):
        return f"{self.full_name} - {self.name}"
