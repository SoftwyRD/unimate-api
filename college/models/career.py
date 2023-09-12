from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from .college import College


class Career(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Career id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    college = models.ForeignKey(
        verbose_name=_("college"),
        help_text=_("College"),
        to=College,
        on_delete=models.CASCADE,
        related_name="careers",
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Career's name"),
        max_length=255,
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        help_text=_("is career active"),
        default=True,
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
        verbose_name = _("career")
        verbose_name_plural = _("careers")
        db_table = "career"

    def __str__(self):
        return f"{self.name} - {self.college.short_name}"

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                if not self.id:
                    self.college.careers_count += 1
                    self.college.save()
                return super().save(*args, **kwargs)
        except Exception:
            raise

    def delete(self, *args, **kwargs):
        self.college.careers_count -= 1
        try:
            with transaction.atomic():
                self.college.save()
                return super().delete(*args, **kwargs)
        except Exception:
            raise
