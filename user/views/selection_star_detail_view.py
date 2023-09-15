from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from selection.models import Selection, SelectionStar
from user.serializers import SelectionStarSerializer

SCHEMA_NAME = "user"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionStarDetailView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = SelectionStar.objects.all()
    serializer_class = SelectionStarSerializer

    @extend_schema(
        operation_id="Star selection",
        description="Star a selection.",
        request=None,
        responses={
            204: None,
        },
    )
    def put(self, request, *args, **kwargs):
        try:
            selection = self.get_selection()
            starred_by = request.user
            _, created = SelectionStar.objects.get_or_create(
                selection=selection, starred_by=starred_by
            )
            if not created:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Selection.DoesNotExist:
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to create your selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Unstar selection",
        description="Unstar a selection.",
    )
    def delete(self, *args, **kwargs):
        try:
            instance = self.get_obj()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SelectionStar.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except Selection.DoesNotExist:
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to create your selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_owner(self):
        owner = self.kwargs.get("owner")
        return get_user_model().objects.get(username__iexact=owner)

    def get_selection(self):
        owner = self.get_owner()
        selection = self.kwargs.get("selection")
        return Selection.objects.get(slug__iexact=selection, owner=owner)

    def get_obj(self):
        selection = self.get_selection()
        return self.queryset.get(
            selection=selection, starred_by=self.request.user
        )

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
