from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserListView().as_view(), name="list"),
    path(
        "<str:owner>/selections/",
        views.UserSelectionsListView().as_view(),
        name="selections",
    ),
    path("profile/", views.ProfileView().as_view(), name="profile"),
]
