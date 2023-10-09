from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from college.models import CollegeModel


class SubjectModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Subject id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    college = models.ForeignKey(
        verbose_name=_("college"),
        help_text=_("College"),
        to=CollegeModel,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    code = models.CharField(
        verbose_name=_("code"),
        help_text=_("Subject code"),
        max_length=7,
    )
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Subject name"),
        max_length=255,
    )
    credits = models.IntegerField(
        verbose_name=_("credits"),
        help_text=_("Subject credits"),
        default=0,
        validators=[MinValueValidator(0)],
    )
    is_lab = models.BooleanField(
        verbose_name=_("is lab"),
        help_text=_("Is this subject a laboratory?"),
        default=False,
    )

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        db_table = "subject"

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)
