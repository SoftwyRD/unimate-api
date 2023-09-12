from django.contrib.admin import ModelAdmin, register

from ..models import Syllabus


@register(Syllabus)
class SyllabusAdmin(ModelAdmin):
    ordering = ("career",)
    list_display = ("career", "year", "is_active", "subjects_count", "credits")
    list_filter = ("is_active",)
    search_fields = (
        "career__name",
        "career__college__short_name",
        "career__college__name",
        "version",
    )
    readonly_fields = ("credits", "subjects_count", "created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "Syllabus information",
            {
                "fields": (
                    "career",
                    "year",
                    "version",
                ),
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
                    "year",
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
