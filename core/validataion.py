

from rest_framework import serializers
from django.core.validators import RegexValidator
from django.utils import timezone
from student.models import Student

def validate_unique_email(value, instance=None):
    qs = Student.objects.filter(email=value)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise serializers.ValidationError("A student with this email already exists.")
    return value


def validate_dob(value):
    today = timezone.now().date()
    if value >= today:
        raise serializers.ValidationError("Date of birth must be in the past.")
    age = (today - value).days // 365
    if age < 3:
        raise serializers.ValidationError("Student must be at least 3 years old.")
    return value


def validate_phone(value):
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    phone_validator(value)
    return value