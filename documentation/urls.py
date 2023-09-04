from django.urls import path
from drf_spectacular import views

app_name = "documentation"

urlpatterns = [
    path("schema/", views.SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "swagger/",
        views.SpectacularSwaggerView.as_view(
            url_name="documentation:api-schema"
        ),
        name="swagger-documentation",
    ),
    path(
        "redoc/",
        views.SpectacularRedocView.as_view(url_name="documentation:api-schema"),
        name="redoc-documentation",
    ),
]
