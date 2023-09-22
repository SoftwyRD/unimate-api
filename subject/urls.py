from django.urls import path

from . import views

app_name = "subject"

urlpatterns = [
    path("", views.SubjectListView.as_view(), name="list"),
    path(
        "<str:college>/<str:subject>/",
        views.SubjectDetailView.as_view(),
        name="detail",
    ),
    path(
        "<str:college>/<str:subject>/sections/",
        views.SubjectSectionListView.as_view(),
        name="section-list",
    ),
    path(
        "<str:college>/<str:subject>/sections/<int:section>/",
        views.SubjectSectionDetailView.as_view(),
        name="section-detail",
    ),
]
