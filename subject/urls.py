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
        "sections/<int:id>/",
        views.SubjectSectionDetailView.as_view(),
        name="sections",
    ),
]
