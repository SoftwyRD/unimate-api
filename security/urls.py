from django.urls import path

from . import views

app_name = "security"

urlpatterns = [
    path("sign-up/", views.SignUpView().as_view(), name="sign-up"),
    path("token/", views.AccessTokenView().as_view(), name="access-token"),
    path(
        "token/refresh/",
        views.RefreshTokenView().as_view(),
        name="refresh-token",
    ),
]
