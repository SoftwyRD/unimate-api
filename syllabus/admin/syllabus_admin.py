from django.contrib.admin import ModelAdmin, register

from ..models import SyllabusModel


@register(SyllabusModel)
class SyllabusAdmin(ModelAdmin):
    ordering = ("career", "-version")
    list_display = (
        "career",
        "version",
        "is_active",
        "cycles_count",
        "subjects_count",
        "credits",
    )
    list_filter = ("is_active",)
    search_fields = (
        "career__name",
        "career__college__name",
        "career__college__full_name",
    )
    readonly_fields = (
        "credits",
        "subjects_count",
        "cycles_count",
        "created_at",
        "modified_at",
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
                    "created_at",
                    "modified_at",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets
