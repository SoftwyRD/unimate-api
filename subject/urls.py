from django.urls import path

from . import views

app_name = "subject"

urlpatterns = [
    path("", views.ListSubjectsView.as_view(), name="list"),
    path("<int:id>/", views.RetrieveSubjectView.as_view(), name="detail"),
    path(
        "sections/<int:id>/",
        views.SubjectSectionDetailView.as_view(),
        name="sections",
    ),
]
