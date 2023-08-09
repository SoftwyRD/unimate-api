from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.models import Selection
from selection.serializers import (
    SelectionSerializer,
)

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SelectionSerializer

    @extend_schema(
        operation_id="Retrieve selection details",
        description="Retrieves the specified selection.",
    )
    def get(self, req, id, format=None):
        """Get a selection for a user"""
        try:
            selection = Selection.objects.filter(id=id)[0]
            serialized = self.serializer_class(selection, many=False)

            if selection and serialized.data["user"] == req.user.id:
                response = {
                    "status": "success",
                    "data": {
                        "selection": serialized.data,
                    },
                }

                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "selection does not exist",
                    "message": "Could not find any matching" + " selection.",
                },
            }

            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update selection",
        description="Partially updates the specified selection.",
    )
    def patch(self, req, id, format=None):
        """Update a selection for a user"""
        try:
            selectionQuery = Selection.objects.filter(id=id)
            if selectionQuery:
                serializedQuerry = self.serializer_class(
                    selectionQuery[0], many=False
                )

            if selectionQuery and serializedQuerry.data["user"] == req.user.id:
                selection = Selection.objects.get(id=id)
                data = dict(req.data)

                data["modified_on"] = datetime.now()
                serializer = self.serializer_class(
                    selection, data=req.data, many=False, partial=True
                )

                if serializer.is_valid():
                    serializer.save()

                    response = {
                        "status": "success",
                        "data": {
                            "selection": serializer.data,
                        },
                    }
                    return Response(response, status.HTTP_200_OK)

                response = {
                    "status": "fail",
                    "data": {
                        "title": "Could not update the selection",
                        "message": serializer.errors,
                    },
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the selection",
                    "message": "Could not find any matching" + " selection.",
                },
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete selection",
        description="Deletes the specified selection.",
    )
    def delete(self, req, id, format=None):
        """Delete a selection for a user"""
        try:
            selection = Selection.objects.filter(id=id)
            if selection:
                serialized = self.serializer_class(selection[0], many=False)

            if selection and serialized.data["user"] == req.user.id:
                selection = Selection.objects.get(id=id)
                selection.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)

            response = {
                "status": "fail",
                "data": {
                    "title": "Selection does not exist",
                    "message": "Could not find any matching" + " selection.",
                },
            }

            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
