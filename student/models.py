from django.db import models
from core.models import BaseModel
from user.models import User
# Create your models here.


class Student(BaseModel):
    """
    Model representing a student.
    """
    user=models.OneToOneField(User , on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    first_name = models.CharField(max_length=30 , null=False , blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30 ,null=False , blank=False)
    gender=models.CharField(max_length=10, choices=[('male','male'),('female','female'),('other','other')], default='other')
    admission_number = models.CharField(max_length=20, unique=True , null=True , blank=False)
    email = models.EmailField(unique=True , null=False , blank=False)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    class_room = models.ForeignKey('school.ClassRoom', verbose_name="Class", on_delete=models.CASCADE, null=True, blank=True , related_name='students')
    address = models.TextField(null=False, blank=False)
    guardian_contact = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=10, unique=True , null=True , blank=False)
    profile_picture = models.ImageField(upload_to='cms/student_profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"