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
        "<uuid:id>/stars/",
        views.SelectionStarDetailView.as_view(),
        name="star",
    ),
    path(
        "<uuid:id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subjects",
    ),
    path(
        "stars/",
        views.SelectionStarListView.as_view(),
        name="starred",
    ),
    path(
        "history/",
        views.SelectionHistoryListView.as_view(),
        name="history",
    ),
]
