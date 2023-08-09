from django.urls import path
from selection import views

app_name = "selection"

urlpatterns = [
    path("", views.SelectionListView.as_view(), name="list"),
    path(
        "<uuid:id>/",
        views.SelectionDetailView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:selection_id>/subjects/",
        views.SubjectSectionListView.as_view(),
        name="subject-list",
    ),
    path(
        "<uuid:selection_id>/sections/<int:subject_section_id>/",
        views.SubjectSectionDetailsView.as_view(),
        name="subject-detail",
    ),
    path(
        "<uuid:selection_id>/sections/<int:subject_section_id>/schedules/",
        views.ScheduleListView.as_view(),
        name="schedule-list",
    ),
]
