from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import SignUpView, ProfileView

app_name = "user"

urlpatterns = [
    path("token/", TokenObtainPairView().as_view(), name="pair-token"),
    path(
        "token/refresh/",
        TokenRefreshView().as_view(),
        name="refresh-token",
    ),
    path("", SignUpView().as_view(), name="sign-up"),
    path("profile/", ProfileView().as_view(), name="profile"),
]
