from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from selection.models import SectionSchedule, Selection, SubjectSection
from selection.serializers import (
    ScheduleSerializer,
)

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class ScheduleListView(APIView):
    serializer_class = ScheduleSerializer

    @extend_schema(
        operation_id="Update subject schedule",
        description="Updates the specified subject schedule.",
    )
    def put(self, request, selection_id, subject_section_id, format=None):
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
            errors = []
            section = SubjectSection.objects.get(id=subject_section_id)
            schedules = list(
                SectionSchedule.objects.filter(section=subject_section_id)
            )

            if len(data) > len(schedules):
                for a in range(len(data) - len(schedules)):
                    schedule = SectionSchedule.objects.create(section=section)
                    schedules.append(schedule)

            for a, schedule in enumerate(schedules):
                try:
                    schedule_data = data[a]
                except IndexError:
                    schedule.delete()
                    continue

                serializer = self.serializer_class(
                    schedule,
                    data=schedule_data,
                    many=False,
                    partial=True,
                )

                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)

            if not errors:
                updated_schedules = SectionSchedule.objects.filter(
                    section=subject_section_id
                )
                serializer = self.serializer_class(
                    updated_schedules,
                    many=True,
                )

                response = {
                    "status": "success",
                    "data": {
                        "schedules": serializer.data,
                    },
                }
                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not update the subject subject",
                    "details": errors,
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
            ex.with_traceback()
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
