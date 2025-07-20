from django.db import models

from core.models import BaseModel

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    established_date = models.DateField()
    # principal = models.ForeignKey('Teacher', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name



class ClassRoom(BaseModel):
    """
    Represents a class/section like '8A', '10B', etc.
    """
    name = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Subject(BaseModel):
    """
    Model representing a subject.
    """
    name = models.CharField(max_length=255, null=False , blank=False , verbose_name="Subject Name")

    description = models.TextField(blank=True, null=True, verbose_name="Description")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']