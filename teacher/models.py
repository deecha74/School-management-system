from django.db import models

from core.models import BaseModel

# Create your models here.


class Teacher(BaseModel):
    """
    Model representing a teacher.
    """
    user=models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True,
        blank=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=False , help_text="This field will be auto generated if not provided.")
    email = models.EmailField(unique=True, null=False, blank=False)
    date_of_birth = models.DateField()
    hire_date = models.DateField(auto_now_add=True)
    subject_specialization = models.CharField(max_length=100)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='cms/teacher_profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def save(self , *args, **kwargs):
        # Custom save logic can be added here if needed
        super().save(*args, **kwargs)
        if not self.employee_id:
            # Generate a unique employee ID if not provided
            self.employee_id = f"EMP-0000{self.id}"
            self.save(update_fields=['employee_id'])
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


