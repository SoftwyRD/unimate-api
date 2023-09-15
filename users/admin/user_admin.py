from collections import OrderedDict

from django.contrib.admin import TabularInline, register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from selection.models import Selection


class SubjectSectionInline(TabularInline):
    model = Selection
    extra = 0
    verbose_name = "selection"
    verbose_name_plural = "selections"


@register(get_user_model())
class UserAdmin(BaseUserAdmin):
    search_help_text = "Username, email, first name and last name."
    show_full_result_count = True
    list_per_page = 25
    date_hierarchy = "date_joined"
    actions = ("activate_user", "deactivate_user")

    ordering = (
        "last_name",
        "first_name",
        "username",
    )
    list_display = (
        "last_name",
        "first_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )

    add_fieldsets = (
        (
            "Personal information",
            {
                "classes": ("extrapretty",),
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            "Auth information",
            {
                "classes": ("extrapretty",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("extrapretty",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Personal information",
            {
                "classes": ("extrapretty",),
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            "Auth information",
            {
                "classes": ("extrapretty",),
                "fields": (
                    "username",
                    "email",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": (
                    "extrapretty",
                    "collapse",
                ),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Others",
            {
                "classes": (
                    "extrapretty",
                    "collapse",
                ),
                "fields": (
                    "date_joined",
                    "last_login",
                ),
            },
        ),
    )

    inlines = (SubjectSectionInline,)

    def activate_user(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} members activated.")

    def deactivate_user(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} members deactivated.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        ordered_actions = OrderedDict(sorted(actions.items()))
        return ordered_actions

    activate_user.short_description = "Activate selected members"
    deactivate_user.short_description = "Deactivate selected members"
