from django.contrib.admin import ModelAdmin, register

from ..models import College


@register(College)
class CollegeAdmin(ModelAdmin):
    ordering = ("short_name", "name")
    list_display = ("short_name", "name", "careers_count")
    search_fields = ("short_name", "name", "syllabuses__name")
    readonly_fields = ("careers_count", "created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "College information",
            {
                "fields": ("name", "short_name"),
            },
        ),
    )

    fieldsets = (
        (
            "College information",
            {
                "fields": ("name", "short_name"),
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
