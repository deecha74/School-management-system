from django.conf import settings
from django.db import models

from core.models import BaseModel
from fee.models import StudentFee
from schoolcms.settings import AUTH_USER_MODEL
from student.models import Student
User=AUTH_USER_MODEL
# Create your models here.

class PaymentMethod(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)  # e.g., Cash, Khalti, Stripe
    description = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    client_id = models.CharField(max_length=250, null=True, blank=True)  # extra data for developers
    public_key = models.CharField(max_length=250, null=True, blank=True)  # extra data for developers
    secret_key = models.CharField(max_length=250, null=True, blank=True)  # extra data for developers
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name



class PaymentHistory(models.Model):
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, related_name="payment_histories")
    reference_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student_fee} - {self.amount_paid}"


class Transaction(BaseModel):
    TRANSACTION_TYPES = (
        ('cash', 'Cash'),
        ('online', 'Online'),
    )

    intent_id = models.CharField(max_length=100, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    # student = models.ForeignKey(  # ✅ NEW: link to the student this transaction is for
    #     Student, 
    #     on_delete=models.CASCADE, 
    #     related_name='transactions'
    # )
    is_completed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='NPR')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    extra_data = models.JSONField(blank=True, null=True)



    def __str__(self):
        return f"{self.intent_id} - {self.transaction_type} - Rs.{self.amount}"
