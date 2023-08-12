from django.urls import path

from . import views

app_name = "selection"

urlpatterns = [
    path("", views.SelectionListView.as_view(), name="list"),
    path(
        "<uuid:id>/",
        views.SelectionDetailView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subjects",
    ),
]
