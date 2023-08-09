from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.models import Selection
from selection.serializers import SelectionSerializer

SCHEMA_NAME = "selections"


def selection_location_url(selection_id):
    return reverse("selection:selection-detail", args=[selection_id])


@extend_schema(tags=[SCHEMA_NAME])
class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectionSerializer

    @extend_schema(
        operation_id="Retrieve selections list",
        description="Retrieves all the selections from the requesting user.",
    )
    def get(self, req, format=None):
        """Get all selections for a user"""
        try:
            selection = Selection.objects.all().filter(user=req.user.id)

            serializer = self.serializer_class(selection, many=True)

            response = {
                "status": "success",
                "data": {
                    "count": selection.count(),
                    "selections": serializer.data,
                },
            }

            return Response(response, status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Create selection",
        description="Retrieves all the selections from the requesting user.",
    )
    def post(self, req, format=None):
        """Create a new selection for a user"""
        try:
            data = req.data

            serializer = self.serializer_class(data=data, many=False)

            if serializer.is_valid():
                serializer.save(user=req.user)

                selection = serializer.data

                headers = {
                    "Location": selection_location_url(selection["id"]),
                }

                response = {
                    "status": "success",
                    "data": {
                        "selection": selection,
                    },
                }
                return Response(
                    response, status.HTTP_201_CREATED, headers=headers
                )

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create selection",
                    "details": serializer.errors,
                },
            }
            print(serializer.errors)
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
