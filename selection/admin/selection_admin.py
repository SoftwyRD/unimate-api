from django.contrib.admin import ModelAdmin, register

from ..models import SelectionModel


@register(SelectionModel)
class SelectionAdmin(ModelAdmin):
    ordering = ("name", "owner")
    list_display = ("name", "owner", "stars_count", "views_count", "is_visible")
    search_fields = ("name", "owner__username")
    readonly_fields = (
        "stars_count",
        "views_count",
        "created_at",
        "modified_at",
    )
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
                "fields": ("is_visible", "owner"),
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
                    "views_count",
                    "stars_count",
                    "is_visible",
                    "owner",
                    "created_at",
                    "modified_at",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("owner",)
        return readonly_fields
