from django.contrib import admin

from teacher.models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'employee_id', 'email',
        'subject_specialization', 'is_active','hire_date'
    )
    search_fields = (
        'user__username', 'email', 'first_name', 'last_name', 'employee_id', 'subject_specialization'
    )
    list_filter = ('subject_specialization', 'is_active', 'date_of_birth', 'hire_date')
    fieldsets = (
        (None, {
            'fields': (
                'user', 'first_name', 'middle_name', 'last_name', 'employee_id',
                'email', 'date_of_birth',  'subject_specialization',
                'address', 'is_active'
            )
        }),
        ('Profile Picture', {'fields': ('profile_picture',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['id', 'employee_id', 'created_at', 'updated_at']

admin.site.register(Teacher, TeacherAdmin)