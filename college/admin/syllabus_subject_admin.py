from django.contrib.admin import ModelAdmin, register

from ..models import SyllabusSubject


@register(SyllabusSubject)
class SyllabusSubjectAdmin(ModelAdmin):
    ordering = ("syllabus",)
    list_display = ("syllabus", "subject", "cycle")
    search_fields = ("syllabus__career__name", "subject__name")
    list_filter = (
        "syllabus__career__name",
        "syllabus__career__college__short_name",
    )
    readonly_fields = ("created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "Subject information",
            {
                "fields": (
                    "syllabus",
                    "subject",
                    "cycle",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Subject information",
            {
                "fields": (
                    "syllabus",
                    "subject",
                    "cycle",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
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
