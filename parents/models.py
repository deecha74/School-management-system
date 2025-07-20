from django.db import models
from core.models import BaseModel
from student.models import Student
# Create your models here.
class Parent(BaseModel):
    """
    Model representing a parent.
    """
    GENDER_CHOICES=(
        ('male','male'),
        ('female','female'),
        ('other','other'),
        ('prefer_not_to_say','prefer not to say')
    )
    user=models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        related_name='parent_profile',
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=30 , null=False , blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30 ,null=False , blank=False)
    email = models.EmailField(unique=True , null=False , blank=False)
    phone_number = models.CharField(max_length=15, unique=True, help_text="Comma-separated phone numbers" , null=True , blank=False)
    address = models.TextField(null=True , blank=True)
    gender=models.CharField(

        choices=GENDER_CHOICES , blank=True, null=True)
    children = models.ManyToManyField(Student, related_name='parents', blank=True)
    profile_picture = models.ImageField(upload_to='cms/parent_profiles/', null=True, blank=True)