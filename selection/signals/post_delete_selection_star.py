from django.db.models.signals import post_delete
from django.dispatch import receiver

from ..models import SelectionStarModel


@receiver(post_delete, sender=SelectionStarModel)
def post_delete_selection_star(sender, instance, **kwargs):
    instance.selection.stars_count -= 1
    instance.selection.save()
