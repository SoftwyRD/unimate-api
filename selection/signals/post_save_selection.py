from django.db.models.signals import post_save
from django.dispatch import receiver

from selection.models import (
    SelectionModel,
    SelectionStarModel,
    ViewHistoryModel,
)


@receiver(post_save, sender=SelectionModel)
def post_save_selection(sender, instance, created, **kwargs):
    if created or instance.is_visible:
        return

    ViewHistoryModel.objects.filter(selection=instance).exclude(
        viewed_by=instance.owner
    ).delete()

    SelectionStarModel.objects.filter(selection=instance).exclude(
        starred_by=instance.owner
    ).delete()
