from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from college.models import CollegeModel

from ..models import SubjectModel
from ..serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectSerializer

    @extend_schema(
        operation_id="Retrieve subject details",
        description="Retrieves the specified subject details",
        responses={
            200: serializer_class,
        },
    )
    def get(self, *args, **kwargs):
        try:
            instance = self.get_obj()
            serializer = self.get_serializer(instance)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except SubjectModel.DoesNotExist:
            response = {
                "title": "Subject does not exist",
                "message": "Could not find any matching subject",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve the subject",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_college(self):
        college = self.kwargs.get("college")
        return CollegeModel.objects.get(name__iexact=college)

    def get_obj(self):
        college = self.get_college()
        subject = self.kwargs.get("subject")
        queryset = self.get_queryset()
        return queryset.get(college=college, code__iexact=subject)

    def get_queryset(self):
        return self.queryset

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
