import csv
from dashboard.forms import PayrollSearchForm, TaskupdateForm
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.db.models import Q, F, FloatField, Sum
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
import datetime
from .models import *
from django.contrib import messages
from employee.forms import DeptCreationForm, EmployeeCreateForm,EmergencyCreateForm,FamilyCreateForm,BankAccountCreation,EmployeeEditForm, PayrollCreationForm
from leave.models import Leave
from employee.models import *
from leave.forms import LeaveCreationForm
from datetime import date, datetime
from accounts.models import User
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from forms.models import RequestForm
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import xlwt
# from leave.forms import CommentForm

@login_required(login_url='/erp/')
def dashboardy(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('accounts:Login')

    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    dash = dashboard.objects.all().order_by('?')[:1]
    staff_leaves = Leave.objects.filter(user = user)
    rf = RequestForm.objects.filter(user = user)
    rfp = rf.filter(status='Pending')
    l = Leave.objects.all()
    allpend = l.filter(status='Pending')
    allapprove = l.filter(status='Approved')
    allreject = l.filter(status='Rejected')
    leaves = staff_leaves.filter(status='Pending')
    aleaves = staff_leaves.filter(status='Approved')
    rleaves = staff_leaves.filter(status='Rejected')
    today = date.today()
    nowe = datetime.now()
    time = nowe.strftime("%H:%M:%S")
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    context = {
        'today': today,
        'employeep':employeep,
        'time': time,
        'employees_birthday': employees_birthday,
        'leaves': leaves,
        'staff_leaves': staff_leaves,
        'aleaves': aleaves,
        'rleaves': rleaves,
        'rf': rf,
        'rfp': rfp,
        'l': l,
        'allapprove': allapprove,
        'allpend': allpend,
        'allreject': allreject,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'dash':dash
    }
    return render(request,'dashboard/dashboard.html',context)

@login_required(login_url='/erp/')
def depcreate(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if request.method == 'POST':
        form = DeptCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.name = request.POST.get('name')
            instance.description = request.POST.get('description')
            instance.save()
            messages.success(request,'Department Succesffuly Added',extra_tags = 'alert alert-success alert-dismissible show')
            return  redirect('dashboard:Employees')
        else:
            messages.error(request, form.errors, extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:DeptAdd')
    form = DeptCreationForm()    
    context = {
        'title': 'Add Department',
        'form': form,
        'employees_birthday':employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request, 'dashboard/deptcreate.html', context)


@login_required(login_url='/erp/')
def dashboard_employees(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    staff_leaves = Leave.objects.filter(user = user)
    rf = RequestForm.objects.filter(user = user)
    rfp = rf.filter(status='Pending')
    l = Leave.objects.all()
    allpend = l.filter(status='Pending')
    allapprove = l.filter(status='Approved')
    allreject = l.filter(status='Rejected')
    leaves = staff_leaves.filter(status='Pending')
    aleaves = staff_leaves.filter(status='Approved')
    rleaves = staff_leaves.filter(status='Rejected')
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    departments = Department.objects.all()
    employees = Employee.objects.all()
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
			Q(firstname__icontains = query) |
			Q(lastname__icontains = query)
		)
    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)
    blocked_employees = Employee.objects.all_blocked_employees()

    context = {
        'employee_list': employees_paginated,
        'departments': departments,
        'all_employees': Employee.objects.all_employees(),
        'blocked_employees':blocked_employees,
        'employees_birthday':employees_birthday,
        'employeep': employeep,
        'staff_leaves': staff_leaves,
        'aleaves': aleaves,
        'rleaves': rleaves,
        'leaves': leaves,
        'rf': rf,
        'rfp': rfp,
        'l': l,
        'allapprove': allapprove,
        'allpend': allpend,
        'allreject': allreject,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,  
    }
    return render(request,'dashboard/employees.html',context)

@login_required(login_url='/erp/')
def dashboard_employees_create(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/')
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id = user)
            
            instance.user = assigned_user
            
            instance.title = request.POST.get('title')
            instance.image = request.POST.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.email = instance.user.email
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            instance.tel = request.POST.get('tel')
            instance.bio = request.POST.get('bio')
            instance.birthday = request.POST.get('birthday')
            
            
            instance.religion = request.POST.get('religion')
            
            instance.nationality = request.POST.get('nationality')
            
            department_id = request.POST.get('department')
            
            department = Department.objects.get(id = department_id)
            
            instance.department = department
            
            instance.hometown = request.POST.get('hometown')
            
            instance.region = request.POST.get('region')
            instance.residence = request.POST.get('residence')
            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            
            instance.lastwork = request.POST.get('lastwork')
            
            instance.position = request.POST.get('position')
            
            instance.ssnitnumber = request.POST.get('ssnitnumber')
            instance.tinnumber = request.POST.get('tinnumber')
            
            instance.role = request.POST.get('role')
            
            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')
            instance.save()
            messages.success(request,'Employee Succesffuly Added',extra_tags = 'alert alert-success alert-dismissible show')
            return  redirect('dashboard:Employees')
        else:
            messages.error(request, form.errors, extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:Employeecreate')
    form = EmployeeCreateForm()
    context = {
        'form': form,
        'employeep': employeep,
        'title': 'Add Employee',
        'subtitle': 'Assign the user created to this Employee',
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/employee_create.html',context)

@login_required(login_url='/erp/')
def employee_edit_data(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated):
        return redirect('/erp/')
    employeed = get_object_or_404(Employee, id = id)
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST or None,request.FILES or None,instance = employeed)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.title = request.POST.get('title')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            instance.bio = request.POST.get('bio')
            instance.birthday = request.POST.get('birthday')
            instance.religion = request.POST.get('religion')
            instance.nationality = request.POST.get('nationality')
            department_id = request.POST.get('department')
            department = Department.objects.get(id = department_id)
            instance.department = department
            instance.hometown = request.POST.get('hometown')
            
            instance.region = request.POST.get('region')
            
            instance.residence = request.POST.get('residence')
            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            instance.lastwork = request.POST.get('lastwork')
            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('ssnitnumber')
            instance.tinnumber = request.POST.get('tinnumber')
            instance.role = request.POST.get('role')
            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now
            instance.save()
            messages.success(request,'Account Updated Successfully !!!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('accounts:Userprofile')
        else:
            messages.error(request,form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:Edit', id=employeed.id)
    form = EmployeeEditForm(request.POST or None,request.FILES or None,instance = employeed)
    context = {
        'form': form,
        'title': 'edit - {0}'.format(employeed.get_full_name),
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/employee_create.html',context)

@login_required(login_url='/erp/')
def dashboard_employee_info(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not request.user.is_authenticated:
        return redirect('/erp/')
    employee = get_object_or_404(Employee, id = id)
    employee_emergency_instance = Emergency.objects.filter(employee = employee).first()
    employee_family_instance = Relationship.objects.filter(employee = employee).first()
    bank = Bank.objects.filter(employee = employee).first()
    context = {
        'employee': employee,
        'employeep': employeep,
        'emergency': employee_emergency_instance,
        'family': employee_family_instance,
        'bank': bank,
        'title': 'profile - {0}'.format(employee.get_full_name),
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/employee_detail.html',context)




# ------------------------- EMERGENCY --------------------------------
@login_required(login_url='/erp/')
def dashboard_emergency_add(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    if request.method == 'POST':
        form = EmergencyCreateForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')
            employee_object = Employee.objects.get(id = employee_id)
            emp_name = employee_object.get_full_name
            instance.employee = employee_object
            
            instance.fullname = request.POST.get('fullname')
            
            instance.tel = request.POST.get('tel')
            instance.location = request.POST.get('location')
            
            instance.relationship = request.POST.get('relationship')
            
            # now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now


            instance.save()
            messages.success(request,'Emergency Information Successfully Added for {0}'.format(emp_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:EmergencyCreate')
        else:
            messages.error(request, form.errors, extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:EmergencyCreate')
    form = EmergencyCreateForm()   
    context = {
        'form': form,
        'title': 'Add Emergency Information',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/emergency_create.html',context)

@login_required(login_url='/erp/')
def dashboard_emergency_update(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    emergency = get_object_or_404(Emergency, id = id)
    employee = emergency.employee
    if request.method == 'POST':
        form = EmergencyCreateForm( data = request.POST, instance = emergency)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee = employee
            instance.fullname = request.POST.get('fullname')
            instance.tel = request.POST.get('tel')
            # now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

	
            instance.location = request.POST.get('location')
            instance.relationship = request.POST.get('relationship')
            '''
				NB: redirect() will try to use its given arguments to reverse a URL. 
				This example assumes your URL patterns contain a pattern like this 
				redirect(assumed_url_name,its_assuemed_whatever_instance id)
			'''
            instance.save()
            messages.success(request,'Emergency Details Successfully Updated',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:Employeeinfo',id = employee.id)# worked on redirect to profile and message success and error
        else:
            messages.error(request, form.errors, extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:EmergencyUpdate')
    form = EmergencyCreateForm(request.POST or None,instance = emergency)
    context = {
        'form': form,
        'title': 'Updating Emergency Details for {0}'.format(employee.get_full_name),
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/emergency_create.html',context)





# ----------------------------- FAMILY ---------------------------------#
# YOU ARE HERE ---- creation form for Family
@login_required(login_url='/erp/')
def dashboard_family_create(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    if request.method == 'POST':
        form = FamilyCreateForm(data = request.POST or None)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee,id = employee_id)
            instance.employee = employee_object
            instance.status = request.POST.get('status')
            instance.spouse = request.POST.get('spouse')
            instance.occupation = request.POST.get('occupation')
            instance.tel = request.POST.get('tel')
            instance.children = request.POST.get('children')
            instance.father = request.POST.get('father')
            instance.foccupation = request.POST.get('foccupation')
            instance.mother = request.POST.get('mother')
            instance.moccupation = request.POST.get('moccupation')
            # now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

            instance.save()
            
            messages.success(request,'Relationship Successfully Created for {0}'.format(employee_object),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:FamilyAdd')
        else:
            messages.error(request, form.errors ,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:FamilyAdd')
        
    form = FamilyCreateForm()
    context = {
        'form': form,
        'title': 'Add Family Infomation',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/family_create_form.html',context)


# HERE FAMILY EDIT
@login_required(login_url='/erp/')
def dashboard_family_edit(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    relation = get_object_or_404(Relationship, id = id)
    employee = relation.employee
    
    if request.method == 'POST':
        form = FamilyCreateForm(data = request.POST, instance = relation)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee = employee
            instance.status = request.POST.get('status')
            instance.spouse = request.POST.get('spouse')
            instance.occupation = request.POST.get('occupation')
            instance.tel = request.POST.get('tel')
            instance.children = request.POST.get('children')
            
            instance.nextofkin = request.POST.get('nextofkin')
            instance.contact = request.POST.get('contact')
            instance.relationship = request.POST.get('relationship')
            instance.father = request.POST.get('father')
            instance.foccupation = request.POST.get('foccupation')
            instance.mother = request.POST.get('mother')
            instance.moccupation = request.POST.get('moccupation')
        
			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			
            instance.save()
            messages.success(request,'Relationship Successfully Updated for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:Employeeinfo', id = employee.id)
        else:
            messages.error(request, form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:FamilyUpdate', id = relation.id)
        
    form = FamilyCreateForm(request.POST or None,instance = relation)
    
    context = {
        'form': form,
        'title': 'Family Information Update',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/family_create_form.html',context)





# BANK 
@login_required(login_url='/erp/')
def dashboard_bank_create(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    if request.method == 'POST':
        form = BankAccountCreation(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee,id = employee_id)
            
            instance.employee = employee_object
            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')
            # now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

            instance.save()
            
            messages.success(request,'Account Successfully Created for {0}'.format(employee_object.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:BankinfoAdd')
        
        else:
            
            messages.error(request,form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:BankinfoAdd')
    form = BankAccountCreation()
    context = {
        'form': form,
        'title': 'Bank Information Create Form',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/bank_account_create_form.html',context)

@login_required(login_url='/erp/')
def employee_bank_account_update(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_authenticated or request.user.is_superuser or request.user.is_staff or request.user.is_HR):
        return redirect('/erp/')
    bank_instance_obj = get_object_or_404(Bank, id = id)
    employee = bank_instance_obj.employee
    
    if request.method == 'POST':
        form = BankAccountCreation(request.POST, instance = bank_instance_obj)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee = employee
            
            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')
            
            
			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

            instance.save()
            
            messages.success(request,'Account Successfully Edited for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:Employeeinfo', id = employee.id)
        else:
            messages.error(request,'Error Updating Account for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:BankinfoAdd')
        
    form = BankAccountCreation(request.POST or None,instance = bank_instance_obj)
    context ={
        'form': form,
        'title' : 'Update Bank Information',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/bank_account_create_form.html',context)





# ---------------------LEAVE-------------------------------------------
@login_required(login_url='/erp/')
def leave_creation(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    myleave = Leave.objects.filter(user = user)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator = Paginator(myleave, 10)
    page = request.GET.get('page')
    myleave = paginator.get_page(page)
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = LeaveCreationForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.user
            instance.user = user
            instance.save()
            
            messages.success(request,'Leave Request Sent,wait for Human Resource Managers response',extra_tags = 'alert alert-success alert-dismissible show')
            
            return redirect('dashboard:CreateLeave')
        
        messages.error(request,form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
        return redirect('dashboard:CreateLeave')
    
    form = LeaveCreationForm()
    context = {
        'form': form,
        'title': 'Apply for Leave',
        'employeep': employeep,
        'myleave': myleave,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/create_leave.html',context)

@login_required(login_url='/erp/')
def pending_leaves_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_staff or request.user.is_superuser or request.user.is_HR):
        return redirect('/erp/')
    leaves = Leave.objects.all_pending_leaves()
    
    paginator = Paginator(leaves, 30)
    page = request.GET.get('page')
    leaves = paginator.get_page(page)
    context = {
        'leave_list':leaves,
        'title':'Leave list - Pending',
        'employeep':employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request,'dashboard/leaves_recent.html',context)

@login_required(login_url='/erp/')
def cancel_leaves_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_staff or request.user.is_superuser or request.user.is_HR):
        return redirect('/erp/')
    leaves = Leave.objects.all_cancel_leaves()
    
    paginator = Paginator(leaves, 30)
    page = request.GET.get('page')
    leaves = paginator.get_page(page)
    context = {
        'leave_list':leaves,
        'title':'Leave list - Cancelled',
        'employeep':employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request,'dashboard/leaves_recent.html',context)

@login_required(login_url='/erp/')
def leaves_approved_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_staff or request.user.is_superuser or request.user.is_HR):
        return redirect('/erp/')
    leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
    
    paginator = Paginator(leaves, 30)
    page = request.GET.get('page')
    leaves = paginator.get_page(page)
    context = {
        'leave_list':leaves,
        'title':'Leave list - Approved',
        'employeep':employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request,'dashboard/leaves_recent.html',context)

@login_required(login_url='/erp/')
def leave_rejected_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_staff or request.user.is_superuser or request.user.is_HR):
        return redirect('/erp/')
    leaves = Leave.objects.all_rejected_leaves()
    
    paginator = Paginator(leaves, 30)
    page = request.GET.get('page')
    leaves = paginator.get_page(page)
    context = {
        'leave_list': leaves,
        'employeep': employeep,
        'title':'Leave list - Rejected',
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/leaves_recent.html',context)

@login_required(login_url='/erp/')
def leaves_view(request,id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_staff or request.user.is_superuser or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    employee = Employee.objects.filter(user = leave.user)[0]
    context = {
        'leave':leave,
        'employee':employee,
        'title':'{0}-{1} leave'.format(leave.user.username,leave.status),
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,    
    }
    return render(request,'dashboard/leave_detail_view.html',context)

@login_required(login_url='/erp/')
def approve_leave(request,id):
    user = request.user
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    user = leave.user
    employee = Employee.objects.filter(user = user)[0]
    leave.approve_leave
    
    messages.success(request,'Leave successfully approved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:UserleaveView', id = id)

@login_required(login_url='/erp/')
def unapprove_leave(request,id):
    user = request.user
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    user = leave.user
    employee = Employee.objects.filter(user = user)[0]
    leave.unapprove_leave
    messages.success(request,'Leave unapproved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:LeavesList') #redirect to unapproved list

@login_required(login_url='/erp/')
def cancel_leave(request,id):
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    leave.leaves_cancel
    
    messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:CanceleavesList')#work on redirecting to instance leave - detail view

@login_required(login_url='/erp/')
def reject_leave(request,id):
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    leave.reject_leave
    messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:LeavesRejected')


# Current section -> here
@login_required(login_url='/erp/')
def uncancel_leave(request,id):
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR):
        return redirect('/erp/')
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'Pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:LeavesList')#work on redirecting to instance leave - detail view

@login_required(login_url='/erp/')
def unreject_leave(request,id):
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'Pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:LeavesList')


# Birthday
@login_required(login_url='/erp/')
def birthday_this_month(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())	
    if not request.user.is_authenticated:
        return redirect('/erp/')
    
    employees_birthday = Employee.objects.birthdays_current_month()
    month = date.today().strftime('%B')#am using this to get the month for template rendering- making it dynamic
    context = {
        'employees_birthday':employees_birthday,
        'month':month,
        'count_birthdays':employees_birthday.count(),
        'title':'Birthdays',
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request,'dashboard/birthdays_this_month.html',context)

@login_required(login_url='/erp/')
def payrollcreate(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR or request.user.is_staff):
        return redirect('/erp/')
    if not (request.user.is_HR or request.user.is_superuser or request.user.is_staff):
        return redirect('dashboard:MyPayrollAll')
    if request.method == 'POST':
        form = PayrollCreationForm(data = request.POST or None)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employ')
            employee_object = get_object_or_404(Employee,id = employee_id)
            bank = Bank.objects.filter(employee = employee_object).first()
            total = float(bank.basic) + float(bank.housing) + float(bank.transport)
            basic_m = float(bank.basic)/12
            housing_m = float(bank.housing)/12
            transport_m = float(bank.transport)/12
            monthly = float(total) / 12
            instance.employ = employee_object
            instance.paymentdate = request.POST.get('paymentdate')
            instance.bank = bank
            instance.overtime = request.POST.get('overtime')
            instance.paye = request.POST.get('paye')
            instance.month = request.POST.get('month')
            instance.Year = request.POST.get('Year')
            instance.loan = request.POST.get('loan')
            instance.bonus = request.POST.get('bonus')
            instance.deductther = request.POST.get('deductther')
            instance.basic_m = round(basic_m)
            instance.housing_m = round(housing_m)
            instance.transport_m = round(transport_m)
            pension = 0.08 * (float(monthly) + float(instance.overtime) + float(instance.bonus))
            instance.pension = round(pension, 2)
            instance.gross = float(monthly) + float(instance.overtime) + float(instance.bonus)
            instance.totald = pension + float(instance.loan) + float(instance.paye)
            instance.netpay = float(instance.gross) - float(instance.totald)

            instance.save()
            
            messages.success(request,'Payroll Successfully Created for {0}'.format(employee_object),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:Payroll')
        else:
            messages.error(request, form.errors ,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:Payroll')
    form = PayrollCreationForm()
    context = {
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'form': form,
        'title': 'Create Payroll',
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render (request, 'dashboard/payroll_create.html' , context)

@login_required(login_url='/erp/')
def edit_payroll(request, id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR or request.user.is_staff):
        return redirect('/erp/')
    payrol = get_object_or_404(Payroll, id = id)
    employee = payrol.employ
    
    if request.method == 'POST':
        form = PayrollCreationForm(data = request.POST, instance = payrol)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employ = employee
            employee_object = get_object_or_404(Employee,id = employee.id)
            bank = Bank.objects.filter(employee = employee_object).first()
            total = float(bank.basic) + float(bank.housing) + float(bank.transport)
            monthly = float(total) / 12
            monthly = round(monthly, 2)
            basic_m = float(bank.basic)/12
            housing_m = float(bank.housing)/12
            transport_m = float(bank.transport)/12
            instance.paymentdate = request.POST.get('paymentdate')
            instance.overtime = request.POST.get('overtime')
            if request.POST.get('overtime') == '':
                instance.overtime = 0
            instance.paye = request.POST.get('paye')
            instance.month = request.POST.get('month')
            instance.Year = request.POST.get('Year')
            instance.loan = request.POST.get('loan')
            if request.POST.get('loan') == '':
                instance.loan = 0
            instance.bonus = request.POST.get('bonus')
            if request.POST.get('bonus') == '':
                instance.bonus = 0
            instance.deductther = request.POST.get('deductther')
            if request.POST.get('deductther') == '':
                instance.deductther = 0
            instance.basic_m = round(basic_m)
            instance.housing_m = round(housing_m)
            instance.transport_m = round(transport_m)
            pension = 0.08 * (float(monthly) + float(instance.overtime) + float(instance.bonus))
            instance.pension = round(pension, 2)
            instance.gross = float(monthly) + float(instance.overtime) + float(instance.bonus)
            instance.totald = pension + float(instance.loan) + float(instance.paye)
            instance.netpay = float(instance.gross) - float(instance.totald)
            instance.save()
            messages.success(request,'Payroll Successfully Edited for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:viewPayrollONE', id = payrol.id)
        else:
            messages.error(request, form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:viewPayrollONE', id = payrol.id)
        
    form = PayrollCreationForm(request.POST or None, instance = payrol)
    
    context = {
        'form': form,
        'title': 'Family Information Update',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/family_create_form.html',context)

@login_required(login_url='/erp/')
def duplicate_payroll(request, id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR or request.user.is_staff):
        return redirect('/erp/')
    payrol = get_object_or_404(Payroll, id = id)
    employee = payrol.employ
    
    if request.method == 'POST':
        form = PayrollCreationForm(data = request.POST, instance = payrol)
        if form.is_valid():
            employ = request.POST.get('employ')
            employe = Employee.objects.get(id = employ)
            employee_object = get_object_or_404(Employee,id = employ)
            bank = Bank.objects.filter(employee = employee_object).first()
            total = float(bank.basic) + float(bank.housing) + float(bank.transport)
            monthly = float(total) / 12
            monthly = round(monthly, 2)
            if request.POST.get('overtime') == ' ':
                overtime = 0
            else:
                overtime = request.POST.get('overtime')
            if request.POST.get('bonus') == ' ':
                bonus = 0
            else:
                bonus = request.POST.get('bonus')
            if request.POST.get('loan') == ' ':
                loan = 0
            else:
                loan = request.POST.get('loan')
            if request.POST.get('deductther') == ' ':
                deductther = 0
            else:
                deductther = request.POST.get('deductther')
            pension = 0.08 * (float(monthly) + float(overtime) + float(bonus))
            gross = float(monthly) + float(overtime) + float(bonus)
            totald = float(pension) + float(loan) + float(request.POST.get('paye'))
            netpay = float(gross) - float(totald)
            Payroll.objects.create(
                employ = employe,
                paymentdate = request.POST.get('paymentdate'),
                overtime = overtime,
                bank = bank, 
                paye = request.POST.get('paye'),
                month = request.POST.get('month'),
                Year = request.POST.get('Year'),
                loan = loan,
                bonus = bonus,
                deductther = deductther,
                pension = round(pension, 2),
                basic_m = float(bank.basic)/12,
                housing_m = float(bank.housing)/12,
                transport_m = float(bank.transport)/12,
                gross = gross,
                totald = totald,
                netpay = netpay
                )
            messages.success(request,'Payroll Successfully created for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:PayrollAll')
        else:
            messages.error(request, form.errors,extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:viewPayrollONE', id = payrol.id)
        
    form = PayrollCreationForm(request.POST or None, instance = payrol)
    
    context = {
        'form': form,
        'title': 'Family Information Update',
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request,'dashboard/family_create_form.html',context)

@login_required(login_url='/erp/')
def payrollall(request):
    if not (request.user.is_superuser or request.user.is_authenticated or request.user.is_HR or request.user.is_staff):
        return redirect('/erp/')
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    pay = Payroll.objects.all().order_by('id')
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    paginator = Paginator(pay, 30)
    page = request.GET.get('page')
    pay = paginator.get_page(page)
    
    
    form = PayrollSearchForm(request.POST or None)
    if request.method == 'POST':
        employ = form['employ'].value()
        month = form['month'].value()
        Year = form['Year'].value()
        pay = Payroll.objects.filter()
        if (employ != ''):
            pay = pay.filter(employ_id=employ)
        
        if (month != ''):
            pay = pay.filter(month=month)
            
        if (Year != ''):
            pay = pay.filter(Year=Year)
            
    
        if form['export_to_EXCEL'].value() == True:
            if (month == ''):
                month = 'All'
            else:
                month = pay.filter().values_list('month', flat=True).first()
                
            if (Year == ''):
                year = ''
            else:
                year = pay.filter().values_list('month', flat=True).first()
            
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="Payroll Schedule for {month} {year}.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Salary Schedule', cell_overwrite_ok=True)
            wse = wb.add_sheet('Salary Schedule2', cell_overwrite_ok=True)
            wba = wb.add_sheet('Bank')
            wp = wb.add_sheet('Payee')
            wpe = wb.add_sheet('Pension')
            wpn = wb.add_sheet('NSITF')
            
            style_bold = 'align: wrap on, vert centre, horiz center; font: bold on;  borders: left_color black, right_color black,\
        left thin, right thin, bottom_color black, bottom thin,; pattern: pattern solid, fore_color white;'

            # ws == Salary Schedule

            ws.col(0).width = int(13*260)
            ws.col(1).width = int(13*260)
            ws.col(2).width = int(13*260)
            ws.col(3).width = int(13*260)
            ws.col(4).width = int(13*260)
            ws.col(5).width = int(13*260)
            ws.col(6).width = int(13*260)
            ws.col(7).width = int(13*260)
            ws.col(8).width = int(13*260)
            ws.col(9).width = int(13*260)
            ws.col(10).width = int(13*260)
            ws.col(11).width = int(13*260)
            ws.col(12).width = int(13*260)
            
            
            ws.write_merge(0, 1, 0, 10, 'Cozym Limited', xlwt.Style.easyxf(style_bold))
            ws.write_merge(2, 2, 0, 10, 'No 3b, Abike Animashaun street, Off Durosimi-Etti street, Lekki Phase 1, Lagos.', xlwt.Style.easyxf(style_bold))
            ws.write_merge(3, 3, 0, 10, f'Salary Schedule for the month ended {month}', xlwt.Style.easyxf(style_bold))
            row_num = 4
            font_style = xlwt.Style.easyxf(style_bold)
            font_style.font.bold = True
            columns = ['Employee Code', 'First name', 'Last name', 'Basic', 'Housing', 'Transport', 'Gross Pay', 'Payee', 'Pension', 'Total Deduction', 'Net Pay']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
                
            row_number = 5
            for payrol in pay:
                ws.write(row_number, 0, payrol.employ.employeeid)
                ws.write(row_number, 1, payrol.employ.firstname)
                ws.write(row_number, 2, payrol.employ.lastname)
                ws.write(row_number, 3, float(payrol.bank.basic)/12)
                ws.write(row_number, 4, float(payrol.bank.housing)/12)
                ws.write(row_number, 5, float(payrol.bank.transport)/12)
                ws.write(row_number, 6, float(payrol.gross))
                ws.write(row_number, 7, float(payrol.paye))
                ws.write(row_number, 8, float(payrol.pension))
                ws.write(row_number, 9, float(payrol.totald))
                ws.write(row_number, 10, float(payrol.netpay))
                row_number+=1
                
            ws.write(row_number + 1, 0, 'Grand Total', font_style)
            ws.write(row_number + 1, 3, xlwt.Formula("SUM(D6:D7)"))
            ws.write(row_number + 1, 4, xlwt.Formula("SUM(E6:E7)"))
            ws.write(row_number + 1, 5, xlwt.Formula("SUM(F6:F7)"))
            ws.write(row_number + 1, 6, xlwt.Formula("SUM(G6:G7)"))
            ws.write(row_number + 1, 7, xlwt.Formula("SUM(H6:H7)"))
            ws.write(row_number + 1, 8, xlwt.Formula("SUM(I6:I7)"))
            ws.write(row_number + 1, 9, xlwt.Formula("SUM(J6:J7)"))
            ws.write(row_number + 1, 10, xlwt.Formula("SUM(K6:K7)"))
            
            # wse salary schedule 2
            
            wse.col(0).width = int(13*260)
            wse.col(1).width = int(13*260)
            wse.col(2).width = int(13*260)
            wse.col(3).width = int(13*260)
            wse.col(4).width = int(13*260)
            wse.col(5).width = int(13*260)
            wse.col(6).width = int(13*260)
            wse.col(7).width = int(13*260)
            wse.col(8).width = int(13*260)
            wse.col(9).width = int(13*260)
            wse.col(10).width = int(13*260)
            wse.col(11).width = int(13*260)
            wse.col(12).width = int(13*260)
            wse.col(13).width = int(13*260)
            wse.col(14).width = int(13*260)
            
            wse.write_merge(0, 1, 0, 10, 'Cozym Limited', xlwt.Style.easyxf(style_bold))
            wse.write_merge(2, 2, 0, 10, 'No 3b, Abike Animashaun street, Off Durosimi-Etti street, Lekki Phase 1, Lagos.', xlwt.Style.easyxf(style_bold))
            wse.write_merge(3, 3, 0, 10, f'Salary Schedule for the month ended {month} (Inclusive)', xlwt.Style.easyxf(style_bold))
            row_num = 4
            font_style = xlwt.Style.easyxf(style_bold)
            font_style.font.bold = True
            columns = ['Employee Code', 'First name', 'Last name', 'Basic', 'Housing', 'Transport', 'Overtime', 'Bonus', 'Loan','Other Deductions' ,'Gross Pay', 'Payee', 'Pension', 'Total Deduction', 'Net Pay']
            
            
            for col_num in range(len(columns)):
                wse.write(row_num, col_num, columns[col_num], font_style)
            
            row_number = 5
            for pays in pay:
                wse.write(row_number, 0, pays.employ.employeeid)
                wse.write(row_number, 1, pays.employ.firstname)
                wse.write(row_number, 2, pays.employ.lastname)
                wse.write(row_number, 3, float(pays.bank.basic)/12)
                wse.write(row_number, 4, float(pays.bank.housing)/12)
                wse.write(row_number, 5, float(pays.bank.transport)/12)
                wse.write(row_number, 6, float(pays.overtime))
                wse.write(row_number, 7, float(pays.bonus))
                wse.write(row_number, 8, float(pays.loan))
                wse.write(row_number, 9, float(pays.deductther))
                wse.write(row_number, 10, float(pays.gross))
                wse.write(row_number, 11, float(pays.paye))
                wse.write(row_number, 12, float(pays.pension))
                wse.write(row_number, 13, float(pays.totald))
                wse.write(row_number, 14, float(pays.netpay))
                row_number+=1
                
            wse.write(row_number + 1, 0, 'Grand Total', font_style)
            wse.write(row_number + 1, 3, xlwt.Formula("SUM(D6:D7)"))
            wse.write(row_number + 1, 4, xlwt.Formula("SUM(E6:E7)"))
            wse.write(row_number + 1, 5, xlwt.Formula("SUM(F6:F7)"))
            wse.write(row_number + 1, 6, xlwt.Formula("SUM(G6:G7)"))
            wse.write(row_number + 1, 7, xlwt.Formula("SUM(H6:H7)"))
            wse.write(row_number + 1, 8, xlwt.Formula("SUM(I6:I7)"))
            wse.write(row_number + 1, 9, xlwt.Formula("SUM(J6:J7)"))
            wse.write(row_number + 1, 10, xlwt.Formula("SUM(K6:K7)"))
            wse.write(row_number + 1, 11, xlwt.Formula("SUM(L6:L7)"))
            wse.write(row_number + 1, 12, xlwt.Formula("SUM(M6:M7)"))
            wse.write(row_number + 1, 13, xlwt.Formula("SUM(N6:N7)"))
            wse.write(row_number + 1, 14, xlwt.Formula("SUM(O6:O7)"))
                    
            #Bank
            wba.col(0).width = int(13*260)
            wba.col(1).width = int(13*260)
            wba.col(2).width = int(13*260)
            wba.col(3).width = int(13*260)
            wba.col(4).width = int(13*260)
            wba.col(5).width = int(13*260)
            
            
            wba.write_merge(0, 1, 0, 10, 'Cozym Limited', xlwt.Style.easyxf(style_bold))
            wba.write_merge(2, 2, 0, 10, 'No 3b, Abike Animashaun street, Off Durosimi-Etti street, Lekki Phase 1, Lagos.', xlwt.Style.easyxf(style_bold))
            wba.write_merge(3, 3, 0, 10, 'Bank', xlwt.Style.easyxf(style_bold))
            
            row_num = 4
            font_style = xlwt.Style.easyxf(style_bold)
            font_style.font.bold = True
            columns = ['Employee Code', 'First name', 'Last name', 'Bank Name', 'Account Number', 'Net Pay']
            
            for col_num in range(len(columns)):
                wba.write(row_num, col_num, columns[col_num], font_style)
            
            row_number = 5
            for payb in pay:
                wba.write(row_number, 0, payb.employ.employeeid)
                wba.write(row_number, 1, payb.employ.firstname)
                wba.write(row_number, 2, payb.employ.lastname)
                wba.write(row_number, 3, payb.bank.name)
                wba.write(row_number, 4, str(payb.bank.account))
                wba.write(row_number, 5, float(payb.netpay))
                row_number+=1
                
            wba.write(row_number + 1, 0, 'Grand Total', font_style)
            wba.write(row_number + 1, 5, xlwt.Formula("SUM(F6:F7)"))
                    
            # Payee
            
            wp.col(0).width = int(13*260)
            wp.col(1).width = int(13*260)
            wp.col(2).width = int(13*260)
            wp.col(3).width = int(13*260)
            wp.col(4).width = int(13*260)
            
            wp.write_merge(0, 1, 0, 10, 'Cozym Limited', xlwt.Style.easyxf(style_bold))
            wp.write_merge(2, 2, 0, 10, 'No 3b, Abike Animashaun street, Off Durosimi-Etti street, Lekki Phase 1, Lagos.', xlwt.Style.easyxf(style_bold))
            wp.write_merge(3, 3, 0, 10, 'Payee', xlwt.Style.easyxf(style_bold))
            
            row_num = 4
            font_style = xlwt.Style.easyxf(style_bold)
            font_style.font.bold = True
            columns = ['Employee Code', 'First name', 'Last name', 'Tax Number', 'Payee']
            
            for col_num in range(len(columns)):
                wp.write(row_num, col_num, columns[col_num], font_style)
            
            row_number = 5
            for paypa in pay:
                wp.write(row_number, 0, paypa.employ.employeeid)
                wp.write(row_number, 1, paypa.employ.firstname)
                wp.write(row_number, 2, paypa.employ.lastname)
                wp.write(row_number, 3, '')
                wp.write(row_number, 4, float(paypa.paye))
                row_number+=1
                
            wp.write(row_number + 1, 0, 'Grand Total', font_style)
            wp.write(row_number + 1, 4, xlwt.Formula("SUM(E6:E7)"))
            
            # Pension
            
            wpe.col(0).width = int(13*260)
            wpe.col(1).width = int(13*260)
            wpe.col(2).width = int(13*260)
            wpe.col(3).width = int(13*260)
            wpe.col(4).width = int(13*260)
            wpe.col(5).width = int(13*260)
            wpe.col(6).width = int(13*260)
            wpe.col(7).width = int(13*260)
            
            
            wpe.write_merge(0, 1, 0, 10, 'Cozym Limited', xlwt.Style.easyxf(style_bold))
            wpe.write_merge(2, 2, 0, 10, 'No 3b, Abike Animashaun street, Off Durosimi-Etti street, Lekki Phase 1, Lagos.', xlwt.Style.easyxf(style_bold))
            wpe.write_merge(3, 3, 0, 10, 'Pension', xlwt.Style.easyxf(style_bold))
            row_num = 4
            
            font_style = xlwt.Style.easyxf(style_bold)
            font_style.font.bold = True
            columns = ['Employee Code', 'First name', 'Last name', 'Pension Number', 'Employee', 'Employer', 'Total']
            
            for col_num in range(len(columns)):
                wpe.write(row_num, col_num, columns[col_num], font_style)
            
            row_number = 5
            for paype in pay:
                wpe.write(row_number, 0, paype.employ.employeeid)
                wpe.write(row_number, 1, paype.employ.firstname)
                wpe.write(row_number, 2, paype.employ.lastname)
                wpe.write(row_number, 3, '')
                wpe.write(row_number, 4, float(paype.pension))
                wpe.write(row_number, 5, float(paype.gross)* 0.10)
                # wpe.write(row_number, 6,  xlwt.Formula("SUM(E6+F7)"))
                wpe.write(row_number, 6, (float(paype.gross)* 0.10) + float(paype.pension))
                row_number+=1
                
            wpe.write(row_number + 1, 0, 'Grand Total', font_style)
            wpe.write(row_number + 1, 4, xlwt.Formula("SUM(E6:E7)"))
            wpe.write(row_number + 1, 5, xlwt.Formula("SUM(F6:F7)"))
            wpe.write(row_number + 1, 6, xlwt.Formula("SUM(G6:G7)"))
            
            wb.save(response)
            return response
    context = {
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'title': 'All Payroll',
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'pay': pay,
        'form': form,
    }
    
    return render (request, 'dashboard/payrollAll.html', context)

@login_required(login_url='/erp/')
def mypayrollall(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    pay = Payroll.objects.filter(employ = employeep)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator = Paginator(pay, 20)
    page = request.GET.get('page')
    payroll_paginated = paginator.get_page(page)
    context = {
        'pay': pay,
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'title': 'My Payroll',
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'pay': payroll_paginated,
    }
    return render (request, 'dashboard/payrollAll.html', context)

@login_required(login_url='/erp/')
def view_onepayroll(request, id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    
    employee = Employee.objects.filter(user = user).first()
    payr = get_object_or_404(Payroll, id=id)
    bank = Bank.objects.filter(employee = payr.employ).first()
    
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    basic = float(bank.basic) / 12
    basicd = f'{basic:,}'
    housing = float(bank.housing) / 12
    housingd = f'{housing:,}'
    transport = float(bank.transport) / 12
    transportd = f'{transport:,}'
    gross = float(basic) + float(housing) + float(transport) + float(payr.overtime) + float(payr.bonus) 
    gross = round(gross, 2)
    grossd = f'{gross:,}'
    payrd = f'{float(payr.paye):,}'
    pensiond = f'{float(payr.pension):,}'
    if payr.loan == '':
        payr.loan = 0
    loaned = f'{float(payr.loan):,}'
    overtimed = f'{float(payr.overtime):,}'
    bonused = f'{float(payr.bonus):,}'
    if payr.deductther == '':
        payr.deductther = 0
    otherdd = f'{float(payr.deductther):,}'
    total = float(payr.paye) + float(payr.pension) + float(payr.loan) + float(payr.deductther)
    total = round(total, 2)
    totald =  f'{float(total):,}'
    net = float(gross) - float(total)
    net = round(net, 2)
    net =  f'{float(net):,}'
    context = {
        'payr': payr,
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'basic': basic,
        'housing': housing,
        'transport': transport,
        'gross': gross,
        'total': total,
        'total': totald,
        'net': net,
        'basicd': basicd,
        'housingd': housingd,
        'transportd': transportd,
        'grossd': grossd,
        'payrd': payrd,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'employee': employee,
        'bank': bank,
        'pensiond': pensiond,
        'loaned': loaned,
        'overtimed': overtimed,
        'bonused': bonused,
        'otherdd': otherdd
    }
    return render (request, 'dashboard/payrollview.html', context)

@login_required(login_url='/erp/')
def render_pdf_viewpayroll(request, id=None):
    user = request.user
    payr = get_object_or_404(Payroll, id=id)
    employee = Employee.objects.filter(user = user).first()
    bank = Bank.objects.filter(employee = payr.employ).first()
    basic = float(bank.basic) / 12
    basicd = f'{basic:,}'
    housing = float(bank.housing) / 12
    housingd = f'{housing:,}'
    transport = float(bank.transport) / 12
    transportd = f'{transport:,}'
    gross = float(basic) + float(housing) + float(transport) + float(payr.overtime) + float(payr.bonus) 
    gross = round(gross, 2)
    grossd = f'{gross:,}'
    payrd = f'{float(payr.paye):,}'
    pensiond = f'{float(payr.pension):,}'
    if payr.loan == '':
        payr.loan = 0
    loaned = f'{float(payr.loan):,}'
    overtimed = f'{float(payr.overtime):,}'
    bonused = f'{float(payr.bonus):,}'
    otherdd = f'{float(payr.otherd):,}'
    total = float(payr.paye) + float(payr.pension) + float(payr.loan) + float(payr.otherd)
    total = round(total, 2)
    totald =  f'{float(total):,}'
    net = float(gross) - float(total)
    net = round(net, 2)
    net =  f'{float(net):,}'
    template_path = 'dashboard/payrollpdf.html'
    context = {
        'payr': payr,
        'basic': basic,
        'housing': housing,
        'transport': transport,
        'gross': gross,
        'total': total,
        'total': totald,
        'net': net,
        'basicd': basicd,
        'housingd': housingd,
        'transportd': transportd,
        'grossd': grossd,
        'payrd': payrd,
        'employee': employee,
        'bank': bank,
        'pensiond': pensiond,
        'loaned': loaned,
        'overtimed': overtimed,
        'bonused': bonused,
        'otherdd': otherdd
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Payslip.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='/erp/')
def download_pdf_viewpayroll(request, id=None):
    payr = get_object_or_404(Payroll, id=id)
    user = request.user
    employee = Employee.objects.filter(user = user).first()
    bank = Bank.objects.filter(employee = payr.employ).first()
    basic = float(bank.basic) / 12
    basicd = f'{basic:,}'
    housing = float(bank.housing) / 12
    housingd = f'{housing:,}'
    transport = float(bank.transport) / 12
    transportd = f'{transport:,}'
    gross = float(basic) + float(housing) + float(transport) + float(payr.overtime) + float(payr.bonus) 
    gross = round(gross, 2)
    grossd = f'{gross:,}'
    payrd = f'{float(payr.paye):,}'
    pensiond = f'{float(payr.pension):,}'
    if payr.loan == '':
        payr.loan = 0
    loaned = f'{float(payr.loan):,}'
    overtimed = f'{float(payr.overtime):,}'
    bonused = f'{float(payr.bonus):,}'
    otherdd = f'{float(payr.otherd):,}'
    total = float(payr.paye) + float(payr.pension) + float(payr.loan) + float(payr.otherd)
    total = round(total, 2)
    totald =  f'{float(total):,}'
    net = float(gross) - float(total)
    net = round(net, 2)
    net =  f'{float(net):,}'
    template_path = 'dashboard/payrollpdf.html'
    context = {
        'payr': payr,
        'basic': basic,
        'housing': housing,
        'transport': transport,
        'gross': gross,
        'total': total,
        'total': totald,
        'net': net,
        'basicd': basicd,
        'housingd': housingd,
        'transportd': transportd,
        'grossd': grossd,
        'payrd': payrd,
        'employee': employee,
        'bank': bank,
        'pensiond': pensiond,
        'loaned': loaned,
        'overtimed': overtimed,
        'bonused': bonused,
        'otherdd': otherdd
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Payslip.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class TaskList(LoginRequiredMixin, ListView):
    login_url='/erp/'
    model = todo
    context_object_name = 'tasks'
    template_name = 'todo/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['tasklist'] = context['tasks'].order_by('complete','duedate')
        context['count'] = context['tasks'].filter(complete=False).count()
        context['employeep'] = Employee.objects.filter(user = self.request.user).first()
        context['employees_birthday'] = Employee.objects.birthdays_current_month()
        context['now'] = datetime.date(datetime.now())
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    login_url='/erp/'
    model = todo
    context_object_name = 'task'
    template_name = 'todo/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    login_url='/erp/'
    model = todo
    fields = ['title', 'description', 'duedate', 'complete']
    success_url = reverse_lazy('dashboard:TodoList')

    def get_form(self, form_class=None):
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(TaskCreate, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'class':'form-control'})
        form.fields['description'].widget = forms.Textarea(attrs={'type':"text", 'class':'form-control'})
        form.fields['duedate'].widget = forms.DateTimeInput(attrs={'type':"date", 'class':'form-control'})
        form.fields['complete'].widget = forms.CheckboxInput()
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    def get(self, *arg, **kwargs):
        user = self.request.user
        employeep = Employee.objects.filter(user = user).first()
        employees_birthday = Employee.objects.birthdays_current_month()
            
        context = {
            'employees_birthday': employees_birthday,
            'employeep': employeep,
            'form': self.get_form,
        }
        return render(self.request, 'todo/task_form.html', context)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url='/erp/'
    model = todo
    fields = ['title', 'description', 'duedate' ,'complete']
    success_url = reverse_lazy('dashboard:TodoList')
    template_name = 'todo/task_form.html'
    
    def get_form(self, form_class=None):
        if form_class is None: 
            form_class = self.get_form_class()
        form = super(TaskUpdate, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'type':"text", 'class':'form-control'})
        form.fields['description'].widget = forms.Textarea(attrs={'type':"text", 'class':'form-control'})
        form.fields['duedate'].widget = forms.DateInput(attrs={'type':"date", 'class':'form-control'})
        form.fields['complete'].widget = forms.CheckboxInput()
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employeep'] = Employee.objects.filter(user = self.request.user).first()
        context['employees_birthday'] = Employee.objects.birthdays_current_month()
        
        return context

class DeleteView(LoginRequiredMixin, DeleteView):
    login_url='/erp/'
    model = todo
    context_object_name = 'task'
    success_url = reverse_lazy('dashboard:TodoList')
    template_name = 'todo/task_confirm_delete.html'
    
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employeep'] = Employee.objects.filter(user = self.request.user).first()
        context['employees_birthday'] = Employee.objects.birthdays_current_month()
        
        return context