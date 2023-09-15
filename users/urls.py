from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.UserListView().as_view(), name="list"),
    path(
        "<str:username>/selections/",
        views.SelectionListView().as_view(),
        name="selections",
    ),
    path(
        "<str:username>/starred/",
        views.StarredSelectionListView().as_view(),
        name="starred",
    ),
]
