from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated , AllowAny
from drf_spectacular.utils import extend_schema
from parents.serializers import ParentSerializer
from .models import Parent
from student.serializers import studentSerializer
# Create your views here.

@extend_schema(tags=["Parents"] , request=studentSerializer, responses=studentSerializer)
class AssociatedChildernView(APIView):
    """
    View to get the associated children of a parent.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            parent = user.parent_profile

            children = parent.children.all()
            serializer = studentSerializer(children, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Parent.DoesNotExist:
            return Response({"error": "Parent profile not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Parents"] , request=ParentSerializer, responses=ParentSerializer)
class ParentProfileView(APIView):
    """
    View to get the parent profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            parent = user.parent_profile
            serializer = ParentSerializer(parent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Parent.DoesNotExist:
            return Response({"error": "Parent profile not found."}, status=status.HTTP_404_NOT_FOUND)