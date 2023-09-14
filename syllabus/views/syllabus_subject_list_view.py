from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from college.models import College
from syllabus.models import Career, SyllabusSubject, Syllabus

from syllabus.serializers import SyllabusSubjectSerializer

SCHEMA_NAME = "syllabuses"


@extend_schema(tags=[SCHEMA_NAME])
class SyllabusSubjectListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = SyllabusSubject.objects.all()
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
        except College.DoesNotExist:
            response = {
                "title": "College does not exist",
                "message": "Could not find any matching college.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Career.DoesNotExist:
            response = {
                "title": "Career does not exist",
                "message": "Could not find any matching career.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Syllabus.DoesNotExist:
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
        return College.objects.get(name__iexact=college)

    def get_career(self):
        college = self.get_college()
        code = self.kwargs.get("code")
        return Career.objects.get(college=college, code__iexact=code)

    def get_syllabus(self):
        career = self.get_career()
        version = self.kwargs.get("version")
        return Syllabus.objects.get(
            career=career, version__iexact=version, is_active=True
        )

    def get_queryset(self):
        syllabus = self.get_syllabus()
        return self.queryset.filter(syllabus=syllabus).order_by("cycle")

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
