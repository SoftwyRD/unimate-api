from django.db.utils import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Selection, SelectionStar
from ..serializers import SelectionStarSerializer

SCHEMA_NAME = "selections"


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
    def post(self, request, id, *args, **kwargs):
        try:
            serializer = self.get_serializer(data={"selection": id})
            if not serializer.is_valid():
                response = {
                    "title": "Could not add the subject section",
                    "message": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            response = serializer.data
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Selection.DoesNotExist:
            response = {
                "title": "Selection does not exist",
                "message": "Could not find any matching selection.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            response = {
                "title": "Could not star selection",
                "message": "You already starred this selection.",
            }
            return Response(response, status.HTTP_304_NOT_MODIFIED)
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
    def delete(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            star = queryset.get(user=request.user)
            star.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SelectionStar.DoesNotExist:
            response = {
                "title": "Could not unstar",
                "message": "You have not starred this selection.",
            }
            return Response(response, status.HTTP_304_NOT_MODIFIED)
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

    def get_queryset(self):
        id = self.kwargs.get("id")
        instance = self.get_obj(id)
        return self.queryset.filter(selection=instance)

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
