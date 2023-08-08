from django.urls import path
from subject.views import ListSubjectsView, RetrieveSubjectView

app_name = "subjects"

urlpatterns = [
    path("", ListSubjectsView.as_view(), name="list"),
    path("<int:id>/", RetrieveSubjectView.as_view(), name="retrieve"),
]
