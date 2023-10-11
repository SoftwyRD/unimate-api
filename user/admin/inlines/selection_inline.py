from django.contrib.admin import TabularInline

from selection.models import SelectionModel


class SelectionInline(TabularInline):
    model = SelectionModel
    extra = 0
    verbose_name = "selection"
    verbose_name_plural = "selections"

    fields = ("name", "views_count", "stars_count", "is_visible")
    readonly_fields = ("name", "views_count", "stars_count")
