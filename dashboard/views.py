from dashboard.decorators import allowed_users, unauthenticated_user, verify_employee
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.files.storage import FileSystemStorage
from scripts.updateEmployees import importEmployeeFile, importStatisticsFile
from .models import *
from .forms import *

@login_required(login_url='login')
def index(request):
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'title': 'Welcome',
        'updates': getUpdates(),
        'important_updates': getImportantUpdates(),
        }
    return render(request, 'dashboard/index.html', context)

def setUpdates():
    global updates
    updates = Updates.objects.all().order_by('-update_date')[:5]

def getUpdates():
    try:
        updates
    except:
        setUpdates()
    return updates

def setImportantUpdates():
    global important_updates
    important_updates = Updates.objects.filter(important=True).order_by('-update_date')[:5]

def getImportantUpdates():
    try:
        important_updates
    except:
        setImportantUpdates()
    return important_updates

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addTimeStats(request, employee_id):
    setEmployee(employee_id)
    TimeStatFormSet = inlineformset_factory(Employee, TimeStats, form=TimeStatsForm, extra=1)
    formset = TimeStatFormSet(queryset=TimeStats.objects.none(), instance=employee)
    if request.method == 'POST':
        formset = TimeStatFormSet(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
            return redirect('detail', employee.employee_id)
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'formset': formset,
        'employee': getGlobalEmployee(),
    }
    return render(request, 'dashboard/timeStats_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addUpdate(request):
    Updates.objects.all().delete()
    update_form = UpdateForms()
    if request.method == 'POST':
        update_form = UpdateForms(request.POST)
        if update_form.is_valid():
            update_form.save()
            return redirect('index')
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'form': update_form,
    }
    return render(request, 'dashboard/update_form.html', context)

@login_required(login_url='login')
@verify_employee
def detail(request, employee_id):
    setGlobalEmployee(employee_id)
    historical_stats = Statistics.objects.filter(employee=employee_id).order_by('-date')[:10]
    historical_qa = QA_Score.objects.filter(employee=employee_id).order_by('-qa_date')[:5]
    if len(historical_stats) != 0:
        recent_acw = historical_stats[0].acw
        recent_aht = historical_stats[0].aht
        recent_call = historical_stats[0].call
        recent_ticket = historical_stats[0].ticket
    else:
        recent_acw, recent_aht, recent_call, recent_ticket = None, None, None, None
    if len(historical_qa) != 0:
        recent_qa = historical_qa[0].qa_score
    else:
        recent_qa = None
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'employee': getGlobalEmployee(),
        'historical_stats': historical_stats,
        'historical_qa': historical_qa, 
        'recent_acw': recent_acw,
        'recent_aht': recent_aht,
        'recent_call': recent_call,
        'recent_ticket': recent_ticket,
        'recent_qa': recent_qa,
        'title': employee,
    }
    return render(request, 'dashboard/detail.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addStats(request, employee_id):
    StatFormSet = inlineformset_factory(Employee, Statistics, form=StatisticsForm, extra=5)
    formset = StatFormSet(queryset=Statistics.objects.none(), instance=employee)
    if request.method == 'POST':
        formset = StatFormSet(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
            return redirect('detail', employee.employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'formset': formset,
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
    }
    return render(request, 'dashboard/stat_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addQA(request, employee_id):
    QAFormSet = inlineformset_factory(Employee, QA_Score, form=QA_ScoreForm, extra=1)
    qa_form = QAFormSet(queryset=QA_Score.objects.none(), instance=employee)
    if request.method == 'POST':
        qa_form = QAFormSet(request.POST, instance=employee)
        if qa_form.is_valid():
            qa_form.save()
            return redirect('detail', employee.employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'qa_form': qa_form,
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
    }
    return render(request, 'dashboard/qa_form.html', context)

@login_required(login_url='login')
def accountSettings(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated for ' + user.first_name)
            return redirect('index')
    context = {
        'form': form,
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'title': 'Update Account',
    }
    return render(request, 'dashboard/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateEmployee(request, employee_id):
    employee = getGlobalEmployee()
    employee_form = EmployeeForm(instance=employee)
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, instance=employee)
        if employee_form.is_valid():
            employee_form.save()
            return redirect('detail', employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'employee_form': employee_form,
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
    }
    return render(request, 'dashboard/update_employee.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateStats(request, pk):
    setStat(pk)
    stat = getStat()
    stat_form = StatisticsForm(instance=stat)
    if request.method == 'POST':
        stat_form = StatisticsForm(request.POST, instance=stat)
        if stat_form.is_valid():
            stat_form.save()
            return redirect('detail', stat.employee.employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'stat_form': stat_form,
    }
    return render(request, 'dashboard/update_stats.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateQA(request, pk):
    setQA(pk)
    qa = getQA()
    qa_form = QA_ScoreForm(instance=qa)
    if request.method == 'POST':
        qa_form =  QA_ScoreForm(request.POST, instance=qa)
        if qa_form.is_valid():
            qa_form.save()
            return redirect('detail', qa.employee.employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'qa_form': qa_form,
    }
    return render(request, 'dashboard/update_qa.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteStats(request, pk):
    setStat(pk)
    stat = getStat()
    stat_form = StatisticsForm(instance=stat)
    if request.method == 'POST':
        stat.delete()
        return redirect('detail', getGlobalEmployee().employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'stat_form': stat_form,
        'stat': stat,
    }
    return render(request, 'dashboard/delete_stats.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteQA(request, pk):
    setQA(pk)
    qa = getQA()
    qa_form = QA_ScoreForm(instance=qa)
    if request.method == 'POST':
        qa.delete()
        return redirect('detail', getGlobalEmployee().employee_id)
    context = {
        'employee': getGlobalEmployee(),
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'qa_form': qa_form,
        'qa': qa,
    }
    return render(request, 'dashboard/delete_qa.html', context)

def setQA(pk):
    global qa
    qa = get_object_or_404(QA_Score, pk=pk)

def getQA():
    return qa

def setStat(pk):
    global stat
    stat = get_object_or_404(Statistics, pk=pk)
    
def getStat():
    return stat

def setGlobalEmployee(employee_id):
    global employee
    employee = get_object_or_404(Employee, pk=employee_id)

def getGlobalEmployee():
    return employee

def setCCAnalysts():
    global current_CC_analyst_list
    current_CC_analyst_list = Employee.objects.filter(role="Analyst", team="CC").order_by('first_name')

def getCCAnalysts():
    try:
        current_CC_analyst_list
    except NameError:
        setCCAnalysts()
    return current_CC_analyst_list

def setCCLeaders():
    global current_CC_leader_list
    current_CC_leader_list = Employee.objects.filter(role="Leader", team="CC").order_by('first_name')

def getCCLeaders():
    try:
        current_CC_leader_list
    except NameError:
        setCCLeaders()
    return current_CC_leader_list

def setCCSpecialists():
    global current_CC_specialist_list
    current_CC_specialist_list = Employee.objects.filter(role="Specialist", team="CC").order_by('first_name')
    
def getCCSpecialists():
    try:
        current_CC_specialist_list
    except NameError:
        setCCSpecialists()
    return current_CC_specialist_list

def setITAnalysts():
    global current_IT_analyst_list
    current_IT_analyst_list = Employee.objects.filter(role="Analyst", team="IT").order_by('first_name')

def getITAnalysts():
    try:
        current_IT_analyst_list
    except NameError:
        setITAnalysts()
    return current_IT_analyst_list

def setITLeaders():
    global current_IT_leader_list
    current_IT_leader_list = Employee.objects.filter(role="Leader", team="IT").order_by('first_name')

def getITLeaders():
    try:
        current_IT_leader_list
    except NameError:
        setITLeaders()
    return current_IT_leader_list

def setITSpecialists():
    global current_IT_specialist_list
    current_IT_specialist_list = Employee.objects.filter(role="Specialist", team="IT").order_by('first_name')
    
def getITSpecialists():
    try:
        current_IT_specialist_list
    except NameError:
        setITSpecialists()
    return current_IT_specialist_list

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def importEmployees(request):
    result = ''
    name = ''
    url = ''
    uploaded = False
    fs = FileSystemStorage()
    if request.method == 'POST':
        file = request.FILES['employee_document']
        file_obj = request.FILES['employee_document'].read().decode('utf-8-sig') 
        result = importEmployeeFile(file_obj)
        name = fs.save(file.name, file) 
        url = fs.url(name)   
        uploaded = True
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'result': result,
        'flag': uploaded,
        'name': name,
        'url': url, 
        }
    return render(request, 'dashboard/import_employees.html', context)
        
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def importStatistics(request):
    result = ''
    name = ''
    url = ''
    uploaded = False
    fs = FileSystemStorage()
    if request.method == 'POST':
        file = request.FILES['statistics_document']
        file_obj = request.FILES['statistics_document'].read().decode('utf-8-sig') 
        result = importStatisticsFile(file_obj)
        name = fs.save(file.name, file) 
        url = fs.url(name) 
        uploaded = True
    context = {
        'current_CC_analyst_list': getCCAnalysts(),
        'current_CC_specialist_list': getCCSpecialists(),
        'current_CC_leader_list': getCCLeaders(),
        'current_IT_analyst_list': getITAnalysts(),
        'current_IT_specialist_list': getITSpecialists(),
        'current_IT_leader_list': getITLeaders(),
        'result': result,
        'flag': uploaded,
        'name': name,
        'url': url, 
        }
    return render(request, 'dashboard/import_statistics.html', context)

@unauthenticated_user
def registerPage(request):
    result = False
    error = None
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            group = setAccess(email)
            if (str(group) == 'admin'):
                result = True
            try:
                user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email, is_superuser=result)
                user.set_password(password)
                user.groups.add(group)
                user.save()
                setEmployee(user)
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
            except Exception as e:
                messages.info(request, 'Account was not created', str(e))
                print("Error in Saving User", str(e))
        else:
            error = form.errors.as_ul
            messages.info(request, 'Account was not created', error)
            print("Error with CreateUserForm", error)
    context = {
        'form': form,
        'error': error,
        }
    return render(request, 'dashboard/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'dashboard/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def setAccess(email):
    ADMIN_EMAILS = [
        'mary.brugger@safelite.com',
        'colton.wharton@safelite.com',
        'holly.robertson@safelite.com',
        'ryan.inskeep@safelite.com',
        'john.richards@safelite.com',
        'ryan.cull@safelite.com',
        'chance.cassady@safelite.com',
        'kimberly.blackburn@safelite.com',
        'jamie.rollins@safelite.com',
    ]
    
    for admin_email in ADMIN_EMAILS:
        if (email.lower() == admin_email.lower()):
            return Group.objects.get(name='admin')
    return Group.objects.get(name='employee')

def setEmployee(user):
    try:
        employee = Employee.objects.get(email=user.email)
        if employee is not None:
            employee.user = user
            employee.save()
        else:
            return
    except Exception as e:
        print("Error in Setting Employee from User Creation", user, str(e))
