# urls.py
from django.urls import path
from .views import StudentFeeListCreateAPIView, MarkFeePaidAPIView

urlpatterns = [
    path('fees/', StudentFeeListCreateAPIView.as_view(), name='fee-list-create'),
    path('fees/<int:fee_id>/pay/', MarkFeePaidAPIView.as_view(), name='mark-fee-paid'),
]