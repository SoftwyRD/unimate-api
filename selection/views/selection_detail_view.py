from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import SelectionModel
from ..permissions import IsOwner
from ..serializers import SelectionSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    queryset = SelectionModel.objects.all()
    serializer_class = SelectionSerializer

    @extend_schema(
        operation_id="Retrieve selection",
        description="Retrieves the specified selection.",
    )
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_obj()
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(instance)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except (
            get_user_model().DoesNotExist,
            SelectionModel.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to retrieve the selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update selection",
        description="Partially updates the specified selection.",
    )
    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_obj()
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
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
        except (
            get_user_model().DoesNotExist,
            SelectionModel.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to update your selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete selection",
        description="Deletes the specified selection.",
    )
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_obj()
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (
            get_user_model().DoesNotExist,
            SelectionModel.DoesNotExist,
            PermissionDenied,
        ):
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

    def get_owner(self):
        owner = self.kwargs.get("owner")
        return get_user_model().objects.get(username__iexact=owner)

    def get_obj(self):
        queryset = self.get_queryset()
        owner = self.get_owner()
        selection = self.kwargs.get("selection")
        return queryset.get(owner=owner, slug__iexact=selection)

    def get_queryset(self):
        return self.queryset

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
