from django.contrib.admin import ModelAdmin, register

from ..models import Selection


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

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("user",)
        return readonly_fields
