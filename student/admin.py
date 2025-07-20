from django.contrib import admin
from .models import Student
# Register your models here.



class StudentAdmin(admin.ModelAdmin):
    list_display = ( 'user','id','first_name','email',"class_room"  )
    search_fields = ('user__username', 'email', 'first_name', 'last_name', 'class_room')
    list_filter = ('class_room', 'date_of_birth')
    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'middle_name', 'last_name', 'admission_number', 'email', 'date_of_birth', 'class_room', 'address', 'roll_number')}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
    )


admin.site.register(Student ,StudentAdmin)