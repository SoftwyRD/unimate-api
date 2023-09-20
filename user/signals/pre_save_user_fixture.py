from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender=get_user_model())
def pre_save_user_fixture(sender, instance, **kwargs):
    raw = kwargs.get("raw")
    if raw:
        instance.date_joined = timezone.now()
