from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "documentation/",
        include("documentation.urls"),
        name="api-documentation",
    ),
    path("users/", include("user.urls"), name="users-resource"),
    path("subjects/", include("subject.urls"), name="subject-resource"),
    path("selections/", include("selection.urls"), name="selection-resource"),
]
