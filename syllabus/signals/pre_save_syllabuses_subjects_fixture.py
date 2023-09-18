from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import SyllabusSubjectModel

from django.utils import timezone


@receiver(pre_save, sender=SyllabusSubjectModel)
def pre_save_syllabuses_subjects_fixture(sender, instance, **kwargs):
    raw = kwargs.get("raw")
    if raw is not None:
        instance.created_at = timezone.now()
        instance.modified_at = timezone.now()
