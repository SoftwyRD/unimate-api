from rest_framework.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views

app_name = "user"

urlpatterns = [
    path("token/", TokenObtainPairView().as_view(), name="pair-token"),
    path(
        "token/refresh/",
        TokenRefreshView().as_view(),
        name="refresh-token",
    ),
    path("", views.SignUpView().as_view(), name="sign-up"),
    path("profile/", views.ProfileView().as_view(), name="profile"),
]
