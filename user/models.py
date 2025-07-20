from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),

    )
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role= models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
    )
    """
    Custom user model that extends the default Django user model.
    """


    def __str__(self):
        return f"{self.username} ({self.role})"