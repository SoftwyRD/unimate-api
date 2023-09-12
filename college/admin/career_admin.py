from django.contrib.admin import ModelAdmin, register

from ..models import Career


@register(Career)
class CareerAdmin(ModelAdmin):
    ordering = ("name",)
    list_display = ("name", "college", "is_active")
    search_fields = ("name", "college__full_name", "college__name")
    readonly_fields = ("created_at", "modified_at")
    show_full_result_count = True
    list_per_page = 25

    add_fieldsets = (
        (
            "Career information",
            {
                "fields": ("name", "college"),
            },
        ),
    )

    fieldsets = (
        (
            "Career information",
            {
                "fields": ("name", "college"),
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
