from django.contrib.admin import TabularInline

from syllabus.models import SyllabusModel


class CareerSyllabusesInline(TabularInline):
    model = SyllabusModel
    extra = 0
    verbose_name = "syllabus"
    verbose_name_plural = "syllabuses"

    ordering = ("-version",)
    fields = ("version", "credits", "subjects_count", "is_active")
    readonly_fields = ("credits", "subjects_count")

    show_change_link = True
