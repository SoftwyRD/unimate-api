from django.contrib.admin import ModelAdmin, register

from ..models import CareerModel

from .inlines import CareerSyllabusesInline


@register(CareerModel)
class CareerAdmin(ModelAdmin):
    ordering = ("name", "college")
    list_display = ("name", "college", "syllabuses_count", "is_active")
    search_fields = ("name", "college__full_name", "college__name")
    list_filter = ("college__name",)
    readonly_fields = ("created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    inlines = (CareerSyllabusesInline,)

    add_fieldsets = (
        (
            "Career information",
            {
                "fields": ("code", "name", "college"),
            },
        ),
    )

    fieldsets = (
        (
            "Career information",
            {
                "fields": ("code", "name", "college"),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "modified_at",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("college",)
        return self.readonly_fields
