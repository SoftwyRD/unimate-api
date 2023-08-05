from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

app_name = "documentation"

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="swagger-documentation",
    ),
]
