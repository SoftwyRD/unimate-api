from django.urls import path

from . import views

app_name = "selection"

urlpatterns = [
    path("", views.SelectionListView.as_view(), name="list"),
    path(
        "<str:owner>/<str:selection>/",
        views.SelectionDetailView.as_view(),
        name="detail",
    ),
    path(
        "<str:owner>/<str:selection>/subjects/",
        views.SelectionSubjectListView.as_view(),
        name="subjects",
    ),
]
