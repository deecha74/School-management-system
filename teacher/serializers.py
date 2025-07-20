
from rest_framework import serializers

from teacher.models import Teacher


class TeacherCreateSerialiser(serializers.ModelSerializer):

    class Meta:
        Model = Teacher
        field='__All__'
