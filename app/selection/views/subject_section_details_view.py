from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.models import Selection, SubjectSection
from selection.serializers import SubjectSectionSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSectionSerializer

    @extend_schema(
        operation_id="Retrieve subject section details",
        description="Retrieves the specified subject section.",
    )
    def get(self, request, selection_id, subject_section_id, format=None):
        """Get subject section details"""
        try:
            user = request.user
            selection = Selection.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you"
                        + " are trying to get the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.get(
                id=subject_section_id, selection=selection_id
            )
            serializer = self.serializer_class(subject_section, many=False)
            response = {
                "status": "success",
                "data": {
                    "subject_section": serializer.data,
                },
            }
            return Response(response, status=status.HTTP_200_OK)

        except SubjectSection.DoesNotExist:
            response = {
                "status": "fail",
                "data": {
                    "title": "Could not find the subject section",
                    "message": "Could not find the subject section you"
                    + " are trying to get.",
                },
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update subject section",
        description="Partially updates the specified subject section.",
    )
    def patch(self, request, selection_id, subject_section_id, format=None):
        """Update subject section details"""
        try:
            user = request.user
            selection = Selection.objects.get(id=selection_id)

            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the selection",
                        "message": "Could not find the selection you are"
                        + " trying to update the subject.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            subject_section = SubjectSection.objects.get(
                id=subject_section_id, selection=selection_id
            )
            serializer = self.serializer_class(
                subject_section, data=data, many=False, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "data": {
                        "subject_section": serializer.data,
                    },
                }
                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the subject subject",
                    "details": serializer.errors,
                },
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)

        except SubjectSection.DoesNotExist:
            response = {
                "status": "fail",
                "data": {
                    "title": "Could not find the subject section",
                    "message": "Could not find the subject section you"
                    + " are trying to get.",
                },
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            response = {
                "status": "error",
                "message": "There was an error trying to update the subjects.",
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete subject section details",
        description="Deletes the specified subject section.",
    )
    def delete(self, request, selection_id, subject_section_id, format=None):
        """Delete subject section"""
        try:
            user = request.user
            selection = Selection.objects.get(id=selection_id)
            if selection.user != user:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not find the subject",
                        "message": "Could not find the subject you are"
                        + " trying to delete.",
                    },
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            subject_section = SubjectSection.objects.get(
                id=subject_section_id, selection=selection_id
            )
            subject_section.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except SubjectSection.DoesNotExist:
            response = {
                "status": "fail",
                "data": {
                    "title": "Could not find the subject section",
                    "message": "Could not find the subject section you"
                    + " are trying to get.",
                },
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            response = {
                "status": "error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
