from rest_framework import serializers
from .models import Parent
from student.models import Student



class ParentSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    class Meta:
        model = Parent
        fields = [
            'first_name', 'middle_name', 'last_name',
            'email',  'phone_number', 'address',
            'profile_picture','children', ]

    def get_children(self, obj):
            children = obj.children.all()
            if not children:
                return []
            return StudentProfileForParentSerializer(children, many=True).data



class StudentProfileForParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name',
            'email', 'class_room', 'roll_number', 'admission_number',
            'profile_picture', 'gender', 'date_of_birth'
        ]

