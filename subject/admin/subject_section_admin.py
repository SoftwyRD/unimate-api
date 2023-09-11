from django.contrib.admin import ModelAdmin, register

from ..models import SubjectSection


@register(SubjectSection)
class SubjectSectionAdmin(ModelAdmin):
    ordering = ("subject",)
    list_display = ("subject", "section")
    list_filter = ("selected_on__is_active",)
    search_fields = (
        "selected_on__selection__name",
        "subject__name",
        "subject__code",
        "selected_on__selection__user__username",
    )
    show_full_result_count = True
    list_per_page = 25

    fieldsets = (
        (
            "Subject section information",
            {
                "fields": (
                    "selection",
                    "section",
                    "subject",
                    "professor",
                    "taken",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ("selection",)
        return readonly_fields
