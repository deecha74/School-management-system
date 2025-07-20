from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from core.utils import IsAdminUser
from drf_spectacular.utils import extend_schema
from .models import Student
from .serializers import *
# Create your views here.
from rest_framework.permissions import IsAuthenticated
User=get_user_model()
@extend_schema(tags=["Student"] , request=StudentCreateSerializer, responses=StudentCreateSerializer)
class StudentCreateApiView(APIView):
    permission_classes = [IsAuthenticated , IsAdminUser]

    def post(self, request, *args, **kwargs):
        # Only admin can create students

        serializer = StudentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,id, *args, **kwargs):
        # Only admin can update students
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentCreateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id , *args , **kwargs):

        try:
            student=Student.objects.get(id=id)
            student.is_active= False  # Soft delete by setting is_active to False
            student.save()
            return Response({"message": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Student"] , request=StudentOnlyUpdateSerializer, responses=StudentOnlyUpdateSerializer)
class StudentOnlyUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Only authenticated users can update their own student profile
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentOnlyUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)