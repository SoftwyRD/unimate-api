from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from selection.models import SelectionModel, SelectionStarModel
from user.serializers import SelectionStarSerializer

SCHEMA_NAME = "user"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionStarDetailView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = SelectionStarModel.objects.all()
    serializer_class = SelectionStarSerializer

    @extend_schema(
        operation_id="Star selection",
        description="Star a selection.",
        request=None,
        responses={
            204: OpenApiResponse(description="Starred successfully."),
            304: OpenApiResponse(
                description="The selection is already starred."
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        try:
            selection = self.get_selection()
            starred_by = request.user
            SelectionStarModel.objects.create(
                selection=selection, starred_by=starred_by
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except SelectionModel.DoesNotExist:
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
        responses={
            204: OpenApiResponse(description="Unstarred successfully."),
            304: OpenApiResponse(
                description="The selection is already unstarred."
            ),
        },
    )
    def delete(self, *args, **kwargs):
        try:
            instance = self.get_obj()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SelectionStarModel.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except SelectionModel.DoesNotExist:
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
        if self.request.user == owner:
            return SelectionModel.objects.get(
                slug__iexact=selection, owner=owner
            )
        return SelectionModel.objects.get(
            slug__iexact=selection, owner=owner, is_visible=True
        )

    def get_obj(self):
        selection = self.get_selection()
        return self.queryset.get(
            selection=selection, starred_by=self.request.user
        )

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
