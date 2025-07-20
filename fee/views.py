from django.conf import settings
from django.shortcuts import render
from datetime import date

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from core.utils import IsAdminUser
from fee.service.email_service import sent_fee_receipt_email
from fee.service.pdf_service import generate_fee_receipt
from .models import StudentFee
from .serializers import StudentFeeSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Fee"] , request=StudentFeeSerializer, responses=StudentFeeSerializer)
class StudentFeeListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        fees = StudentFee.objects.all()
        serializer = StudentFeeSerializer(fees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentFeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(tags=["Fee"] , request=StudentFeeSerializer, responses=StudentFeeSerializer)
class MarkFeePaidAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, fee_id):
        try:
            fee = StudentFee.objects.get(id=fee_id)
        except StudentFee.DoesNotExist:
            return Response({"error": "Fee not found"}, status=404)

        if fee.is_paid:
            return Response({"message": "Already paid."}, status=400)

        fee.is_paid = True
        fee.paid_on = date.today()
        fee.save()

        pdf_path=generate_fee_receipt(fee)

        subject = f"Fee Receipt: {fee.fee_type.name}"
        message = (
            f"Dear {fee.student.first_name},\n\n"
            f"Your payment for '{fee.fee_type.name}' has been successfully recorded.\n"
            f"Please find your receipt attached.\n\n"
            f"Thank you.\n\n- School Admin"
        )

        # Send to student and parent (if user & email exist)
        if fee.student.user and fee.student.user.email:
            sent_fee_receipt_email(fee.student.user.email, subject, message, pdf_path)

        if fee.student.parent and fee.student.parent.user and fee.student.parent.user.email:
            sent_fee_receipt_email(fee.student.parent.user.email, subject, message, pdf_path)

        return Response({
            "message": "Fee marked as paid and receipt emailed.",
            "pdf_url": f"{settings.MEDIA_URL}{pdf_path}"
        }, status=200)