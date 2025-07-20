 
from django.db import models
from django.utils.text import slugify
from core.models import Month
from student.models import Student

# Create your models here.



class FeeType(models.Model):
    name = models.CharField(max_length=50)  # e.g., Tuition, Exam Fee
    description = models.TextField(blank=True)
    default_amount = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length = 50 , null=True)


    def __str__(self):
        return self.name

    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)

        super().save(*args, **kwargs)


class StudentFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_fees")
    fee_type = models.ForeignKey(FeeType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(null=True, blank=True , help_text="Date when the fee was paid")
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, help_text="Month for which the fee is applicable and year is the current year")
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.fee_type.name}"


