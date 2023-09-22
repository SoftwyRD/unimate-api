from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserView().as_view(), name="profile"),
    path(
        "history/",
        views.SelectionHistoryListView.as_view(),
        name="history",
    ),
    path("password/", views.PasswordView().as_view(), name="password"),
    path(
        "starred/",
        views.SelectionStarListView.as_view(),
        name="starred",
    ),
    path(
        "starred/<str:owner>/<str:selection>/",
        views.SelectionStarDetailView.as_view(),
        name="starred",
    ),
    path(
        "selections/",
        views.SelectionsListView().as_view(),
        name="selections",
    ),
]
