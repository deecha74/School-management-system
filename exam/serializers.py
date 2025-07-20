
from rest_framework import serializers
from exam.models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'  # Adjust fields as necessary
        read_only_fields = ['id']  # Specify read-only fields if needed