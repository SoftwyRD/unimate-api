from django.urls import path

from . import views

app_name = "subject_section"

urlpatterns = [
    path("<int:id>/", views.SubjectSectionDetailView.as_view(), name="detail"),
]
