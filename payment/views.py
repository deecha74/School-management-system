import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from fee.models import StudentFee
from payment.client.khalti import KhaltiClient
from .models import PaymentHistory, PaymentMethod, Transaction
from .serializers import PaymentSerializer
from drf_spectacular.utils import extend_schema
import requests
# Create your views here.

@extend_schema(tags=["Payment"] , request=PaymentSerializer, responses=PaymentSerializer)
class PaymentMethodAPIView(APIView):

    def get(self , request):
        payment=PaymentMethod.objects.all()
        serializers=PaymentSerializer(payment , many = True)
        return Response (serializers.data ,status = status.HTTP_200_OK)

    def post(self , request , *args, **kwargs):
        serializer=PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)

        return Response(serializer.error , status=status.HTTP_400_BAD_REQUEST)




@extend_schema(tags=["Payment"])
class createKhaltiTransactionAPIView(APIView):
    def post(self , request):
        amount= request.data.get('amount')
        customer_info = request.data.get("customer_info")
        order_name = request.data.get("order_name")


        try:
            client = KhaltiClient(
                public_key=settings.KHALTI_PUBLIC_KEY,
                secret_key=settings.KHALTI_SECRET_KEY,
                sandbox=True
            )

            result = client.create_intent(
                amount=amount,
                customer_info=customer_info,
                fee_details={"order_name": order_name}
            )

            pidx = result.get("pidx")
            # respnse_json=result.json()
            # pidx = respnse_json.get('pidx')
        
            payment_url = result.get("payment_url")
            payment_method = PaymentMethod.objects.get(slug='khalti')
            Transaction.objects.create(
                intent_id=pidx,
                sender=request.user,
                receiver_id=settings.DEFAULT_UUID,
                amount=amount,
                currency="NPR",
                transaction_type="online",
                extra_data=result

            )

    
            return Response({
                    "message": "Khalti intent created",
                    "pidx": pidx,
                    "payment_url": payment_url
                }, status=200)

        except Exception as e:
            return Response({'error':str(e)} , status= status.HTTP_400_BAD_REQUEST)




class KhaltiVerifyPaymentAPIView(APIView):
    def post(self, request):
        pidx = request.data.get('pidx')
        student_id = request.data.get('student_id')

        if not pidx:
            return Response({"error": "Missing pidx"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1️⃣ Use sandbox URL if you are testing
            lookup_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
            headers = {
                "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                lookup_url,
                headers=headers,
                json={"pidx": pidx}
            )

            print("Khalti Verification Response:", response.status_code, response.text)

            response.raise_for_status()
            status_data = response.json()

            if status_data.get('status') == 'Completed':
                # ✅ Mark transaction
                transaction = get_object_or_404(Transaction, intent_id=pidx, sender=request.user)
                transaction.is_completed = True
                transaction.save()

                # ✅ Mark student fee paid
                student = get_object_or_404(StudentFee, student_id=student_id)
                student.is_paid = True
                student.paid_on = datetime.datetime.now()
                student.due_date = None
                student.remarks = "Payment completed via Khalti. Thank you."
                student.save()

                # ✅ Actually create payment history
                payment_history = PaymentHistory.objects.create(
                    student_fee= student,
                    amount_paid=transaction.amount,
                    method=PaymentMethod.objects.get(slug='khalti'),
                    reference_number=str([pidx, transaction.id])
                )

                return Response({
                    "message": "Payment verified successfully. Fees marked as paid.",
                    "payment_history_id": payment_history.id  # ✅ return real ID
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    "message": "Payment not completed.",
                    "status": status_data.get('status')  # ✅ use Khalti's actual status, NOT the module
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
