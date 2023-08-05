from django.contrib import admin
from selection.models import (
    Selection,
    SubjectSection,
    SectionSchedule,
    Weekday,
)


admin.site.register(Selection)
admin.site.register(SubjectSection)
admin.site.register(SectionSchedule)
admin.site.register(Weekday)
