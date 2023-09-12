from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    path("admin/", admin.site.urls, name="admin"),
    path("auth/", include("security.urls"), name="security"),
    path("colleges/", include("college.urls"), name="college"),
    path(
        "documentation/",
        include("documentation.urls"),
        name="api-documentation",
    ),
    path("selections/", include("selection.urls"), name="selection-resource"),
    path("subjects/", include("subject.urls"), name="subject-resource"),
    path("users/", include("user.urls"), name="users-resource"),
)
