from django.contrib import admin

from payment.models import PaymentHistory

from .models import FeeType, StudentFee

# Register your models here.


admin.site.register(FeeType)  # Register your models here, if any.

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'due_date', 'is_paid', 'month')
    list_filter = ('month', 'fee_type', 'is_paid')
    search_fields = ('student__first_name', 'student__last_name')
    
# admin.site.register(PaymentHistory)  # Register your models here, if any.
