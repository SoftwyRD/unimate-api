from django.contrib.admin import TabularInline

from ...models import SectionSchedule


class SectionScheduleInline(TabularInline):
    model = SectionSchedule
    extra = 0
    verbose_name = "schedule"
    verbose_name_plural = "schedules"
