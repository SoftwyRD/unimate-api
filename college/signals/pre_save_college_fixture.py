from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import CollegeModel

from django.utils import timezone


@receiver(pre_save, sender=CollegeModel)
def pre_save_college_fixture(sender, instance, **kwargs):
    raw = kwargs.get("raw")
    if raw:
        instance.created_at = timezone.now()
        instance.modified_at = timezone.now()
