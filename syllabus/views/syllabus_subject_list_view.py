from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from college.models import CollegeModel, CareerModel
from syllabus.models import SyllabusSubjectModel, SyllabusModel

from syllabus.serializers import SyllabusSubjectSerializer

SCHEMA_NAME = "syllabuses"


@extend_schema(tags=[SCHEMA_NAME])
class SyllabusSubjectListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = SyllabusSubjectModel.objects.all()
    serializer_class = SyllabusSubjectSerializer

    @extend_schema(
        operation_id="Retrieve a syllabus",
        description="Retrieve a syllabus.",
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except CollegeModel.DoesNotExist:
            response = {
                "title": "College does not exist",
                "message": "Could not find any matching college.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except CareerModel.DoesNotExist:
            response = {
                "title": "Career does not exist",
                "message": "Could not find any matching career.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except SyllabusModel.DoesNotExist:
            response = {
                "title": "Syllabus does not exist",
                "message": "Could not find any matching syllabus.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_college(self):
        college = self.kwargs.get("college")
        return CollegeModel.objects.get(name__iexact=college)

    def get_career(self):
        college = self.get_college()
        career = self.kwargs.get("career")
        return CareerModel.objects.get(college=college, code__iexact=career)

    def get_syllabus(self):
        career = self.get_career()
        version = self.kwargs.get("version")
        return SyllabusModel.objects.get(
            career=career, version__iexact=version, is_active=True
        )

    def get_queryset(self):
        syllabus = self.get_syllabus()
        return self.queryset.filter(syllabus=syllabus).order_by("cycle")

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
