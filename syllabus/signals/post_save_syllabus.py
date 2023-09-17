from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SyllabusModel


@receiver(post_save, sender=SyllabusModel)
def post_save_syllabus(sender, instance, created, **kwargs):
    if instance.latest:
        syllabus = sender.objects.filter(
            career=instance.career, latest=True
        ).exclude(id=instance.id)
        if syllabus.exists():
            syllabus.update(latest=False)

    if created:
        instance.career.syllabuses_count += 1
        instance.career.save()
