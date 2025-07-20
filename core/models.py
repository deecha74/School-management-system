from django.utils import timezone
from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class Month(models.Model):
    """
    Model to represent a month.
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    year = models.IntegerField()

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)