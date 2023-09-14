from django.urls import path

from . import views

app_name = "syllabus"

urlpatterns = [
    path(
        "<str:college>/<str:code>/",
        views.SyllabusListView.as_view(),
        name="list",
    ),
    path(
        "<str:college>/<str:code>/subjects/<str:version>/",
        views.SyllabusSubjectListView.as_view(),
        name="subjects",
    ),
]
