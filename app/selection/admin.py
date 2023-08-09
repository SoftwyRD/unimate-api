from django.contrib import admin
from selection.models import (
    SectionSchedule,
    Selection,
    SubjectSection,
    Weekday,
)

admin.site.register(Selection)
admin.site.register(SubjectSection)
admin.site.register(SectionSchedule)
admin.site.register(Weekday)
