from django.contrib.admin import ModelAdmin, register

from ..models import College
from .inlines import CareersInline


@register(College)
class CollegeAdmin(ModelAdmin):
    ordering = ("name", "full_name")
    list_display = ("name", "full_name", "careers_count")
    search_fields = ("name", "full_name", "syllabuses__name")
    readonly_fields = ("careers_count", "created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    inlines = (CareersInline,)

    add_fieldsets = (
        (
            "College information",
            {
                "fields": ("name", "full_name"),
            },
        ),
    )

    fieldsets = (
        (
            "College information",
            {
                "fields": ("name", "full_name"),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "careers_count",
                    "created_at",
                    "modified_at",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return self.fieldsets
