from django.apps import AppConfig


class CareerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "syllabus"

    def ready(self):
        from . import signals
