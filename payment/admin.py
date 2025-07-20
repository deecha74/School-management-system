from django.contrib import admin

from payment.models import *

# Register your models here.

admin.site.register(Transaction)
admin.site.register(PaymentHistory)
admin.site.register(PaymentMethod)