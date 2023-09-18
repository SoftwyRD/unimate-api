from django.db.models.signals import post_delete
from django.dispatch import receiver

from ..models import SyllabusModel


@receiver(post_delete, sender=SyllabusModel)
def post_delete_syllabus(sender, instance, created, **kwargs):
    instance.career.syllabuses_count -= 1
    instance.career.save()
