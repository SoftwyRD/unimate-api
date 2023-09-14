from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserListView().as_view(), name="list"),
    path("profile/", views.ProfileView().as_view(), name="profile"),
    path(
        "profile/selections/",
        views.ProfileSelectionsListView().as_view(),
        name="profile-selections",
    ),
    path(
        "<str:owner>/selections/",
        views.UserSelectionsListView().as_view(),
        name="selections",
    ),
]
