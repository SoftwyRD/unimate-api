from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Selection
from ..permissions import IsOwner
from ..serializers import SelectionDetailSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer

    @extend_schema(
        operation_id="Retrieve selection details",
        description="Retrieves the specified selection.",
    )
    def get(self, request, id, *args, **kwargs):
        try:
            instance = self.queryset.get(id=id)
            self.check_object_permissions(request, instance)
            serializer = self.serializer_class(instance)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except (Selection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "status": "Internal error",
                "message": "There was an error trying to retrieve the selection.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update selection",
        description="Partially updates the specified selection.",
    )
    def patch(self, request, id, *args, **kwargs):
        try:
            instance = self.queryset.get(id=id)
            self.check_object_permissions(request, instance)
            data = request.data
            user = request.user
            context = {"user": user}
            serializer = self.serializer_class(
                instance, data=data, partial=True, context=context
            )
            if not serializer.is_valid():
                response = {
                    "title": "Could not update the selection",
                    "message": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except (Selection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to update your selection.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete selection",
        description="Deletes the specified selection.",
    )
    def delete(self, request, id, *args, **kwargs):
        try:
            instance = self.queryset.get(id=id)
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Selection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to delete the section.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
