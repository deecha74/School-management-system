from django.contrib import admin
from .models import Parent
# Register your models here.

class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'first_name', 'email')
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'middle_name', 'last_name','gender', 'email', 'phone_number')}),
        ('Address', {'fields': ('address',)}),
        ('Relationships', {'fields': ('children',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),


    )

admin.site.register(Parent , ParentAdmin)