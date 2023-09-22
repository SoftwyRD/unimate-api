from django.contrib.admin import ModelAdmin, register

from ..models import SyllabusSubjectModel


@register(SyllabusSubjectModel)
class SyllabusSubjectAdmin(ModelAdmin):
    ordering = ("subject", "-syllabus", "cycle")
    list_display = ("subject", "syllabus", "cycle")
    search_fields = ("syllabus__career__name", "subject__name")
    list_filter = (
        "syllabus__career__name",
        "syllabus__career__college__name",
    )
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
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets
