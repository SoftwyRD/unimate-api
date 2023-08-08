from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from subject.models import Subject
from subject.serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class ListSubjectsView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        operation_id="Retreave subjects list",
        description="Retrieves all the subjects.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
