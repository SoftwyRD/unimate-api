from django.db.models.signals import post_delete
from django.dispatch import receiver

from ..models import CareerModel


@receiver(post_delete, sender=CareerModel)
def post_delete_career(sender, instance, created, **kwargs):
    instance.college.careers_count -= 1
    instance.college.save()
