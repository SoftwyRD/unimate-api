from django.contrib.admin import ModelAdmin, register, site

from .models import Subject, SectionSchedule, Weekday, SubjectSection


@register(Subject)
class SubjectAdmin(ModelAdmin):
    ordering = ["code"]
    list_display = ["code", "name", "is_lab"]
    list_filter = ["is_lab"]
    search_fields = ["code", "name"]
    fieldsets = (
        (
            "Subject information",
            {
                "fields": (
                    "code",
                    "name",
                    "credits",
                    "is_lab",
                ),
            },
        ),
    )


site.register(SectionSchedule)
site.register(Weekday)
site.register(SubjectSection)
