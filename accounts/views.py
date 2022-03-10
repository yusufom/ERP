from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserLogin
from employee.models import *
from .forms import UserLogin, UserAddForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from dashboard.views import todo
import datetime
from datetime import date, datetime

# Create your views here.
@login_required(login_url='/erp/')
def changepassword(request):
    user = request.user
    employee = Employee.objects.filter(user = user).first()
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not request.user.is_authenticated:
        return redirect('/erp/')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request,user)
            
            messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
            return redirect('accounts:Changepassword')
        else:
            messages.error(request,form.errors,extra_tags = 'alert alert-warning alert-dismissible show' )
            return redirect('accounts:Changepassword')
    
    form = PasswordChangeForm(request.user)
    context = {
        'form':form, 
        'employee':employee,
        'employeep': employeep,
        'employees_birthday': employees_birthday,
            'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request,'accounts/changepassword.html',context)

@login_required(login_url='/erp/')
def register_user_view(request):
    user = request.user
    employee = Employee.objects.filter(user = user).first()
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if request.method == 'POST':
        form = UserAddForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            username = form.cleaned_data.get("username")
            
            messages.success(request,'Account created for {0} !'.format(username),extra_tags = 'alert alert-success alert-dismissible show' )
            return redirect('dashboard:Employeecreate')
        else:
            messages.error(request, form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('accounts:Register')
    form = UserAddForm()
    context = {
        'form': form,
        'employee': employee,
        'employeep': employeep,
            'employees_birthday': employees_birthday,
            'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        
    }
    return render(request,'accounts/register.html',context)

def account_login(request):
    login_user = request.user
    if request.method == 'POST':
        form = UserLogin(data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user and user.is_active:
                login(request,user)
                if login_user.is_authenticated:
                    return redirect('dashboard:Dash')
            else:
                messages.error(request,'Username or Password is incorrect, Try again or Contact Admin',extra_tags = 'alert alert-warning alert-dismissible show' )
                return redirect('accounts:Login') 
        else:
            return HttpResponse('data not valid')
    form = UserLogin()
    context = {
        'form':form,
        
    }
    return render(request,'accounts/login.html',context)

@login_required(login_url='/erp/')
def user_profile_view(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if user.is_authenticated:
        employee = Employee.objects.filter(user = user).first()
        emergency = Emergency.objects.filter(employee = employee).first()
        relationship = Relationship.objects.filter(employee = employee).first()
        bank = Bank.objects.filter(employee = employee).first()
        
        context = {
            'employee':employee,
            'emergency': emergency,
            'family':relationship,
            'bank': bank,
            'employeep': employeep,
            'employees_birthday': employees_birthday,
            'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
        return render(request,'dashboard/employee_detail.html',context)
    return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")

@login_required(login_url='/erp/')
def logout_view(request):
	logout(request)
	return redirect('accounts:Login')