from rest_framework import serializers

from payment.models import PaymentMethod

class PaymentSerializer(serializers.SerializerMethodField):

    class Meta:
        model=PaymentMethod
        fields = '__all__'
