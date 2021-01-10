from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'mobile', 'email', 'hire_date', 'birthdate', 'role', 'team')
    list_filter = ('first_name', 'last_name', 'hire_date', 'birthdate',  'role', 'team')
    search_fields = ('first_name', 'last_name', 'employee_id',  'mobile', 'email', 'hire_date', 'birthdate', 'role', 'team', 'avaya_login', 'ext')
admin.site.register(Employee, EmployeeAdmin)

