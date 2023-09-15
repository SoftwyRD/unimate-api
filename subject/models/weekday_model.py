from django.db import models
from django.utils.translation import gettext_lazy as _


class WeekdayModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Weekday id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Weekday name"),
        max_length=10,
        unique=True,
    )

    class Meta:
        verbose_name = _("weekday")
        verbose_name_plural = _("weekdays")
        db_table = "weekday"

    def __str__(self):
        return self.name
