from django.db.models.signals import pre_delete
from django.dispatch import receiver

from selection.models import SelectionModel


@receiver(pre_delete, sender=SelectionModel)
def pre_delete_selection(sender, instance, created, **kwargs):
    instance.career.selections_count -= 1
    instance.career.save()
