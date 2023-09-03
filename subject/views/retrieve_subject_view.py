from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Subject
from ..serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class RetrieveSubjectView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @extend_schema(
        operation_id="Retrieve subject details",
        description="Retrieves the specified subject details.",
        responses={
            200: serializer_class,
        },
    )
    def get(self, request, id, *args, **kwargs):
        try:
            instance = self.queryset.get(id=id)
            serializer = self.serializer_class(instance)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Subject.DoesNotExist:
            response = {
                "title": "Subject does not exist",
                "message": "Could not find any matching subject.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve the subject.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)