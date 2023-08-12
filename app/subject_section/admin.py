from django.contrib import admin

from .models import SectionSchedule, Weekday, SubjectSection

admin.site.register(SectionSchedule)
admin.site.register(Weekday)
admin.site.register(SubjectSection)
