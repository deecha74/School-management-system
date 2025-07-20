from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils import IsAdminUser, IsTeacherUser
from exam.models import Exam
from exam.serializers import ExamSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Exam"] , request=ExamSerializer, responses=ExamSerializer)
class ExamCreateAPIView(APIView):
    """
    API view to create a new exam.

    """
    permission_classes = [IsAdminUser, IsTeacherUser]
    
    def post(self, request, *args, **kwargs):

            serializer = ExamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Exam"] , request=ExamSerializer, responses=ExamSerializer)
class ExamUpdateAPIView(APIView):
    """
    API view to update an existing exam.

    """
    permission_classes = [ IsTeacherUser , IsAdminUser]

    def put(self, request, *args, **kwargs):
        exam_id = kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        if not exam:
            return Response({"detail": "Exam not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExamSerializer(exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Exam"] )
class ExamDeleteAPIView(APIView):
    """
    API view to delete an existing exam.

    """
    permission_classes = [IsAuthenticated , IsTeacherUser]

    def delete(self, request, *args, **kwargs):
        exam_id = kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        if not exam:
            return Response({"detail": "Exam not found."}, status=status.HTTP_404_NOT_FOUND)
        exam.delete()
        return Response({"detail": "Exam deleted successfully."}, status=status.HTTP_204_NO_CONTENT)