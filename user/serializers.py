
from user.models import User
from rest_framework import serializers
import re
from django.contrib.auth import authenticate
from user.utils import cleanup_email
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name' , 'password', 'role' ,'date_joined', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'default': True},
        }
        read_only_fields = ['id']


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'student'},
        }

    def validate_email(self, email : str):
        """
        Validate that the email is unique.
        """
        if not len(email) :
            raise serializers.ValidationError("Email is required.")
        email=cleanup_email(email)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")


        return email

    def validate_password(self, password: str):
        """
        Validate that the password is at least 8 characters long.
        """
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        if not re.match(r"^(?=.*?\w)(?=.*?[#?!@$%^&*\"'()\\/{}]).{8,}$", password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        return password


    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'student'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    # print("username")
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data