from django.contrib import admin

from school.models import ClassRoom, School, Subject

# Register your models here.

admin.site.register(ClassRoom)
admin.site.register(School)
admin.site.register(Subject)