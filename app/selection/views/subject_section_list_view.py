from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.models import Selection, SubjectSection
from selection.serializers import SubjectSectionSerializer

SCHEMA_NAME = "selections"


def subject_section_location_url(selection_id, subject_section_id):
    return reverse(
        "selection:subject-detail", args=[selection_id, subject_section_id]
    )


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSectionSerializer

    @extend_schema(
        operation_id="Retrieve subject sections list",
        description="Retrieves all the subject sections from the specified selection.",
    )
    def get(self, request, selection_id, format=None):
        """Get all subject sections"""
        try:
            user = request.user
            selection = Selection.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find selection",
                        "message": "Could not find any matching"
                        + " selections to add this subject section.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.filter(
                selection=selection
            )
            serializer = self.serializer_class(subject_section, many=True)

            response = {
                "status": "success",
                "data": {
                    "count": subject_section.count(),
                    "subject_sections": serializer.data,
                },
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            print(e)
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Add subject section",
        description="Adds a subject section to the specified selections.",
    )
    def post(self, request, selection_id, format=None):
        """Create a subject section"""
        try:
            user = request.user
            selection = Selection.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you are"
                        + " trying to add the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            data = request.data

            serializer = self.serializer_class(data=data, many=False)

            if serializer.is_valid():
                serializer.save(selection=selection)
                subject_section = serializer.data

                headers = {
                    "Location": subject_section_location_url(
                        selection_id, subject_section["id"]
                    ),
                }
                response = {
                    "status": "success",
                    "data": {
                        "subject_section": subject_section,
                    },
                }
                return Response(
                    response, status.HTTP_201_CREATED, headers=headers
                )

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create the subject section",
                    "message": serializer.errors,
                },
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "status": "error",
                "message": "There was an error trying to post the subjects.",
            }
            print("Exception:")
            print(e)
            e.__traceback__()
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
