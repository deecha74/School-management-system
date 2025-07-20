# serializers.py
from rest_framework import serializers
from .models import StudentFee

class StudentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFee
        fields = '__all__'
        read_only_fields = ['is_paid', 'paid_on']
