from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import SubjectSection
from ..permissions import IsOwner
from ..serializers import SubjectSectionSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SubjectSection.objects.all()
    serializer_class = SubjectSectionSerializer

    @extend_schema(
        operation_id="Retrieve subject section details",
        description="Retrieves the specified subject section.",
    )
    def get(self, request, id, *args, **kwargs):
        try:
            instance = self.get_obj(id)
            self.check_object_permissions(request, instance)
            context = self.get_serializer_context(
                request=request, instance=instance
            )
            serializer = self.get_serializer(instance, context=context)
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except (SubjectSection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Section does not exists",
                "message": "Could not find a matching section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve the subject.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update subject section",
        description="Partially updates the specified subject section.",
    )
    def patch(self, request, id, *args, **kwargs):
        try:
            instance = self.get_obj(id)
            self.check_object_permissions(request, instance)
            context = self.get_serializer_context(
                request=request, instance=instance
            )
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True,
                context=context,
            )
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except (SubjectSection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Could not find the subject section",
                "message": "Could not find a matching subject section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to update the subject.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete subject section details",
        description="Deletes the specified subject section.",
    )
    def delete(self, request, id, *args, **kwargs):
        try:
            instance = self.get_obj(id)
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (SubjectSection.DoesNotExist, PermissionDenied):
            response = {
                "title": "Could not find the subject section",
                "message": "Could not find a matching subject section.",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to delete the subject.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_obj(self, id):
        queryset = self.get_queryset()
        return queryset.get(id=id)

    def get_queryset(self):
        return self.queryset

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)

    def get_selection(self, request, instance):
        selections = instance.selections.get(selection__user=request.user)
        return selections.selection

    def get_serializer_context(self, **kwargs):
        request = kwargs.pop("request")
        instance = kwargs.pop("instance")
        selection = self.get_selection(request, instance)
        return {"selection": selection}
