from django.urls import path

from . import views

app_name = "college"

urlpatterns = [
    path("", views.CollegeListView.as_view(), name="list"),
    path(
        "<int:id>/careers/",
        views.CollegeCareerListView.as_view(),
        name="careers",
    ),
    path(
        "<int:id>/syllabuses/",
        views.CollegeSyllabusListView.as_view(),
        name="syllabuses",
    ),
]
