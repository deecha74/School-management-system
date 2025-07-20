from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from school.models import ClassRoom, Subject
from school.serializers import ClassRoomSerializer, SubjectSerializer


@extend_schema(tags=["School"] , request=ClassRoomSerializer, responses=ClassRoomSerializer)
class ClassRoomApiView(APIView):

    def get(self, request, *args, **kwargs):
        classrooms = ClassRoom.objects.all()
        serializer = ClassRoomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ClassRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, id, **kwargs):
        try:
            classroom = ClassRoom.objects.get(id=id)
            classroom.delete()
            return Response({"message": "Classroom deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ClassRoom.DoesNotExist:
            return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["School"] , request=SubjectSerializer, responses=SubjectSerializer)
class SubjectApiView(APIView):

    def get(self, request, *args, **kwargs):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, id, **kwargs):
        try:
            subject = Subject.objects.get(id=id)
            subject.delete()
            return Response({"message": "Subject deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)