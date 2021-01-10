from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Employee

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def verify_employee(view_func):
    def wrapper_func(request, *args, **kwargs):
        result = False
        groups = request.user.groups.all()
        for group in groups:
            if group.name == 'admin':
                result = True
        employee_id = request.path.replace('/', '')
        try:
            employee = Employee.objects.get(pk=employee_id)
            if ((employee.email.lower() == request.user.email.lower()) or (result)):
                return view_func(request, *args, **kwargs)    
            else:
                return redirect('index')
        except Exception as e:
            print("Error in verifying Employee before authorizing content", view_func, request, 'Error:' + str(e))
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func