
from django.core.management.base import BaseCommand
from core.models import Month
from fee.models import FeeType, StudentFee
from student.models import Student
from datetime import date


class Command(BaseCommand):
    help = "Create monthly fee for all students"


    
    def handle(self, *args, **kwargs):
       

        today = date.today()
        month_name = today.strftime("%B")  # e.g., "June"
        year = today.year

        current_month = Month.objects.get(name=month_name, year=year)
        print ('Current Month:', current_month)
        fee_type=FeeType.objects.get(name="Tution")   

        students = Student.objects.all()
        for student in students:
            # Assuming StudentFee has a method to create monthly fee
            StudentFee.objects.get_or_create(student=student, month=current_month , amount=5000 , fee_type=fee_type, due_date=today, defaults={'remarks': 'Monthly fee for ' + month_name})
            #
            self.stdout.write(self.style.SUCCESS(f"Monthly fee created for {student.first_name}"))

        
        self.stdout.write(self.style.SUCCESS("Monthly fees created for all students."))

        

       