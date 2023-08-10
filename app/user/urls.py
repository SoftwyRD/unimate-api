from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.SignUpView().as_view(), name="sign-up"),
    path("profile/", views.ProfileView().as_view(), name="profile"),
    path("token/", views.PairTokenView().as_view(), name="pair-token"),
    path(
        "token/refresh/",
        views.RefreshTokenView().as_view(),
        name="refresh-token",
    ),
]
