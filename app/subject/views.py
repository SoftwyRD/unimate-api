from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Subject as SubjectModel
from subject.serializers import SubjectSerializer
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


class SubjectsListView(views.APIView):
    """View for list subjects in api"""
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated]

    serializer = SubjectSerializer

    def get(self, req, format=None):
        try:
            subjects = SubjectModel.objects.all()
            serializer = self.serializer(subjects, many=True)
            response = {
                "status": "success",
                "data": {
                    "count": subjects.count(),
                    "subjects": serializer.data,
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, req, format=None):
        try:
            data = req.data
            serializer = self.serializer(data=data, many=False)

            if serializer.is_valid():
                serializer.save()
                subject = serializer.data

                response = {
                    "status": "success",
                    "data": {
                        "subject": subject,
                    },
                }
                return Response(response, status.HTTP_201_CREATED)

            response = {
                "status": "fail",
                "data": {
                    "title": "Could not create this subject",
                    "message": serializer.errors,
                },
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            response = {
                "status": "error",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectDetailView(views.APIView):
    """
    View for GET, PUT and PATCH subject details
    """
    serializer = SubjectSerializer

    def get(self, req, code, format=None):
        try:
            code = code.upper()
            if SubjectModel.objects.filter(code=code):
                subject = SubjectModel.objects.get(code=code)
                serializer = self.serializer(subject, many=False)

                response = {
                    "status": "success",
                    "data": {
                        "subject": serializer.data,
                    },
                }

                return Response(response, status.HTTP_200_OK)

            response = {
                "status": "error",
                "data": {
                    "message": "Subject does not exist",
                },
            }

            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            response = {
                "status": "fail",
                "message": ex,
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
