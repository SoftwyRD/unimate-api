from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from subject.serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class RetrieveSubjectView(RetrieveAPIView):
    serializer_class = SubjectSerializer
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        operation_id="Retreave subject details",
        description="Retrieves the specified subject details.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
