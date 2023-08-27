from django.contrib.admin import ModelAdmin, TabularInline, register
from subject.models import SubjectSection

from ..models import Selection


class SubjectSectionInline(TabularInline):
    model = SubjectSection
    extra = 0
    verbose_name = "section"
    verbose_name_plural = "sections"


@register(Selection)
class SelectionAdmin(ModelAdmin):
    ordering = ("name", "user")
    list_display = ("name", "user")
    search_fields = ("name", "user__username")
    readonly_fields = ("created", "modified")
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "Selection information",
            {
                "fields": ("name",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("user",),
            },
        ),
    )

    fieldsets = (
        (
            "Selection information",
            {
                "fields": ("name",),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "user",
                    "created",
                    "modified",
                ),
            },
        ),
    )

    inlines = (SubjectSectionInline,)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("user",)
        return readonly_fields
