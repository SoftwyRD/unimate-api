from django.contrib.admin import ModelAdmin, register

from ..models import SubjectSection
from .inlines import SectionScheduleInline


@register(SubjectSection)
class SubjectSectionAdmin(ModelAdmin):
    ordering = ("subject", "-section", "-cycle", "-year")
    list_display = ("subject", "section", "cycle", "year")
    list_filter = ("selections__is_active",)
    search_fields = (
        "selections__selection__name",
        "subject__name",
        "subject__code",
        "selections__selection__user__username",
    )
    show_full_result_count = True
    list_per_page = 25

    inlines = (SectionScheduleInline,)

    fieldsets = (
        (
            "Section information",
            {
                "fields": (
                    "subject",
                    "section",
                    "professor",
                    "cycle",
                    "year",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("selection",)
        return readonly_fields
