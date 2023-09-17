from django.db.models.signals import pre_delete
from django.dispatch import receiver

from ..models import SyllabusModel


@receiver(pre_delete, sender=SyllabusModel)
def pre_delete_syllabus(sender, instance, created, **kwargs):
    instance.career.syllabuses_count -= 1
    instance.career.save()
