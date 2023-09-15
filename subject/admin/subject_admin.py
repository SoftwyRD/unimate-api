from django.contrib.admin import ModelAdmin, register

from ..models import Subject


@register(Subject)
class SubjectAdmin(ModelAdmin):
    ordering = ("code",)
    list_display = ("code", "name", "college", "is_lab")
    list_filter = (
        "college__name",
        "is_lab",
    )
    search_fields = ("code", "name")
    show_full_result_count = True
    list_per_page = 25

    fieldsets = (
        (
            "Subject information",
            {
                "fields": (
                    "college",
                    "code",
                    "name",
                    "credits",
                    "is_lab",
                ),
            },
        ),
    )
