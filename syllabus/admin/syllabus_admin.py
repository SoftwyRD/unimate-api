from django.contrib.admin import ModelAdmin, register

from ..models import SyllabusModel


@register(SyllabusModel)
class SyllabusAdmin(ModelAdmin):
    ordering = ("career__name", "-version")
    list_display = (
        "career",
        "version",
        "cycles_count",
        "subjects_count",
        "credits",
        "is_active",
        "latest",
    )
    list_filter = ("is_active", "latest")
    search_fields = (
        "career__name",
        "career__college__name",
        "career__college__full_name",
    )
    readonly_fields = (
        "credits",
        "subjects_count",
        "cycles_count",
        "latest",
    )
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "Syllabus information",
            {
                "fields": ("career", "version"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("is_active",),
            },
        ),
    )

    fieldsets = (
        (
            "Syllabus information",
            {
                "fields": (
                    "career",
                    "version",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "credits",
                    "subjects_count",
                    "cycles_count",
                    "is_active",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets
