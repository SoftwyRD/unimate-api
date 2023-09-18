from django.contrib.admin import TabularInline

from ...models import CareerModel


class CareersInline(TabularInline):
    model = CareerModel
    extra = 0
    verbose_name = "career"
    verbose_name_plural = "careers"

    ordering = ("code",)
    fields = ("code", "name", "syllabuses_count", "is_active")
    readonly_fields = ("syllabuses_count",)

    show_change_link = True
