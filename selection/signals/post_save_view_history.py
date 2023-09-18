from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import ViewHistoryModel


@receiver(post_save, sender=ViewHistoryModel)
def post_save_view_history(sender, instance, **kwargs):
    instance.selection.views_count += 1
    instance.selection.save()
