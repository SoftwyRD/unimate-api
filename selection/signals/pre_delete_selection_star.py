from django.db.models.signals import pre_delete
from django.dispatch import receiver

from ..models import SelectionStarModel


@receiver(pre_delete, sender=SelectionStarModel)
def pre_delete_selection_star(sender, instance, **kwargs):
    instance.selection.stars_count -= 1
    instance.selection.save()
