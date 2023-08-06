from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

app_name = "documentation"

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="documentation:api-schema"),
        name="swagger-documentation",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="documentation:api-schema"),
        name="redoc-documentation",
    ),
]
