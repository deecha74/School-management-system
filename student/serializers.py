from core.validataion import validate_dob, validate_phone, validate_unique_email
from .models import Student
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime


class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'first_name', 'middle_name', 'last_name', 'gender',
            'admission_number', 'email', 'date_of_birth', 'enrollment_date',
            'class_room', 'address', 'guardian_contact', 'roll_number',
            'profile_picture', 'is_active'
        ]
        read_only_fields = ['id', 'enrollment_date']

    def validate_email(self, value):
        return validate_unique_email(value, self.instance)

    def validate_admission_number(self, value):
        if value is None:
            raise serializers.ValidationError("Admission number is required.")
        if Student.objects.filter(admission_number=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Admission number must be unique.")
        return value

    def validate_roll_number(self, value):
        if value is None:
            raise serializers.ValidationError("Roll number is required.")
        if Student.objects.filter(roll_number=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Roll number must be unique.")
        return value

    def validate_guardian_contact(self, value):
        return validate_phone(value, self.instance)

    def validate_date_of_birth(self, value):
        return validate_dob(value, self.instance)




class StudentOnlyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'profile_picture', 'email',]