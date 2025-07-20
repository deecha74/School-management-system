from django.urls import path
from .views import KhaltiVerifyPaymentAPIView, PaymentMethodAPIView, createKhaltiTransactionAPIView

urlpatterns = [
    path('payment-methods/', PaymentMethodAPIView.as_view(), name='payment-methods'),
    path('khalti/', createKhaltiTransactionAPIView.as_view(), name='khalti payment '),
    path('khalti/verify/', KhaltiVerifyPaymentAPIView.as_view(), name='khalti verification'),
]