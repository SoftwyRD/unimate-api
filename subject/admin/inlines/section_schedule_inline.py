from django.contrib.admin import TabularInline

from ...models import SectionScheduleModel


class SectionScheduleInline(TabularInline):
    model = SectionScheduleModel
    extra = 0
    verbose_name = "schedule"
    verbose_name_plural = "schedules"
