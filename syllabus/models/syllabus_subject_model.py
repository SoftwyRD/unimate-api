from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from subject.models import SubjectModel

from .syllabus_model import SyllabusModel


class SyllabusSubjectModel(models.Model):
    id = models.AutoField(
        verbose_name=_("id"),
        help_text=_("Syllabus subject id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    syllabus = models.ForeignKey(
        verbose_name=_("syllabus"),
        help_text=_("Syllabus"),
        to=SyllabusModel,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    subject = models.ForeignKey(
        verbose_name=_("subject"),
        help_text=_("Syllabus' subject"),
        to=SubjectModel,
        on_delete=models.CASCADE,
        related_name="syllabuses",
    )
    cycle = models.IntegerField(
        verbose_name=_("cycle"),
        help_text=_("Cycle on syllabus"),
        validators=[MinValueValidator(0)],
        default=1,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("Creation date"),
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name=_("modified at"),
        help_text=_("Modified date"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        db_table = "syllabus_subject"

        unique_together = ("syllabus", "subject")

    def __str__(self):
        return (
            f"{self.syllabus.career.name} ({self.syllabus.version}) - "
            + f"{self.syllabus.career.college.name} | {self.subject}"
        )

    def save(self, *args, **kwargs):
        credits_count = 0
        cycles_count = self.cycle

        if not self.id:
            self.syllabus.subjects_count += 1
            credits_count = self.subject.credits

        for syllabus in SyllabusSubjectModel.objects.filter(
            syllabus=self.syllabus
        ):
            if syllabus.id == self.id:
                credits_count += self.subject.credits - syllabus.subject.credits

            credits_count += syllabus.subject.credits
            if syllabus.cycle > cycles_count:
                cycles_count = syllabus.cycle

        self.syllabus.cycles_count = cycles_count
        self.syllabus.credits = credits_count
        try:
            with transaction.atomic():
                self.syllabus.save()
                return super().save(*args, **kwargs)
        except Exception:
            raise

    def delete(self, *args, **kwargs):
        self.syllabus.credits -= self.subject.credits
        self.syllabus.subjects_count -= 1

        syllabus = SyllabusSubjectModel.objects.order_by("cycles_count").first()
        self.syllabus.cycles_count = syllabus.syllabus.cycles_count

        try:
            with transaction.atomic():
                self.syllabus.save()
                return super().delete(*args, **kwargs)
        except Exception:
            raise
