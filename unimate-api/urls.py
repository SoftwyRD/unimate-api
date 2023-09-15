from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    path("admin/", admin.site.urls, name="admin"),
    path("auth/", include("security.urls"), name="security"),
    path("colleges/", include("college.urls"), name="colleges"),
    path(
        "documentation/",
        include("documentation.urls"),
        name="api-documentation",
    ),
    path("selections/", include("selection.urls"), name="selections"),
    # path("subjects/", include("subject.urls"), name="subjects"),
    path("syllabuses/", include("syllabus.urls"), name="syllabuses"),
    path("user/", include("user.urls"), name="user"),
    path("users/", include("users.urls"), name="users"),
)
