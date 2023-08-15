from django.contrib.admin import ModelAdmin, TabularInline, register

from ..models import SectionSchedule, SubjectSection


class SectionScheduleInline(TabularInline):
    model = SectionSchedule
    extra = 0
    verbose_name = "schedule"
    verbose_name_plural = "schedules"


@register(SubjectSection)
class SubjectSectionAdmin(ModelAdmin):
    ordering = ("selection",)
    list_display = ("selection", "subject", "section")
    list_filter = ("taken",)
    search_fields = (
        "selection__name",
        "subject__name",
        "subject__code",
        "selection__user__username",
    )
    show_full_result_count = True
    list_per_page = 25

    fieldsets = (
        (
            "Subject section information",
            {
                "fields": (
                    "selection",
                    "section",
                    "subject",
                    "professor",
                    "taken",
                ),
            },
        ),
    )

    inlines = (SectionScheduleInline,)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("selection",)
        return readonly_fields
