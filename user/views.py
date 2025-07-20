from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from user.serializers import UserLoginSerializer, UserSignUpSerializer


@extend_schema(tags=["User"] , request=UserSignUpSerializer, responses=UserSignUpSerializer)
class userSignupAPIView(APIView):
    """
    API view for user signup.
    """
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    "message": "User signup success!",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["User"] , request=UserLoginSerializer, responses=UserLoginSerializer)
class userLoginAPIView(APIView):
    """
    API view for user login.
    """
    def post(self, request):
        serializers = UserLoginSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if "@" in username:
            user = User.objects.filter(email__iexact=username).first()
        else:
            user     = User.objects.filter(username__iexact=username).first()
        if serializers.is_valid():
            user=serializers.validated_data['user']
            if not user.is_active:
                return Response({'detail': 'Your account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)
            refresh= RefreshToken.for_user(user)

            return Response({
            'user': user.username,
            'role': user.role,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
