from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import CareerModel


@receiver(post_save, sender=CareerModel)
def post_save_career(sender, instance, created, **kwargs):
    if created:
        instance.college.careers_count += 1
        instance.college.save()
