from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SelectionStarModel


@receiver(post_save, sender=SelectionStarModel)
def post_save_selection_star(sender, instance, created, **kwargs):
    if created:
        instance.selection.stars_count += 1
        instance.selection.save()
