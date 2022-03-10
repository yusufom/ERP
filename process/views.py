from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import CriticalConstantsAndAFIOC, DensityOfIOL, ElementAll, EnthalpyandGibbs, HeatCapacityAtConstantPOIOLhyperbolic, HeatCapacityAtConstantPOIOLpolynomial, HeatCapacityOIOL, HeatofVaporizationOIOL, ThermalConductivityofIOL, VaporPressureOfIOL, VaporThermalofIOS, VaporViscosityIOS, ViscosityofIOL
from employee.models import Employee
from django.db.models import Q
from .forms import ElementSearchForm
from dashboard.models import todo
import datetime
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='/erp/')
def pro_home(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    queryset = ElementAll.objects.all().order_by('id')
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    form = ElementSearchForm(request.POST or None)
    if request.method == 'POST':
        compound = form['compound'].value()
        element = form['element'].value()
        queryset = ElementAll.objects.filter(
									name__icontains=form['name'].value(),
									)
        if (compound != ''):
            queryset = queryset.filter(compound_id=compound)
        
        
        if (element != ''):
            queryset = queryset.filter(element_id=element)
    context = {
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        "queryset": queryset,
        'form': form,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        
    }
    return render (request, 'process/pro.html', context)

@login_required(login_url='/erp/')
def element_detail(request, id):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    ele = get_object_or_404(ElementAll, id = id)
    vpiol = VaporPressureOfIOL.objects.filter(el = ele).first()
    diol = DensityOfIOL.objects.filter(el = ele).first()
    ccioc = CriticalConstantsAndAFIOC.objects.filter(el = ele).first()
    hviol = HeatofVaporizationOIOL.objects.filter(el = ele).first()
    hciol = HeatCapacityOIOL.objects.filter(el = ele).first()
    hccpiolp = HeatCapacityAtConstantPOIOLpolynomial.objects.filter(el = ele).first()
    hccpiolh = HeatCapacityAtConstantPOIOLhyperbolic.objects.filter(el = ele).first()
    eandg = EnthalpyandGibbs.objects.filter(el = ele).first()
    vvios = VaporViscosityIOS.objects.filter(el = ele).first()
    viol = ViscosityofIOL.objects.filter(el = ele).first()
    vtios = VaporThermalofIOS.objects.filter(el = ele).first()
    tciol = ThermalConductivityofIOL.objects.filter(el = ele).first()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    context = {
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'ele': ele,
        'vpiol': vpiol,
        'diol': diol,
        'ccioc': ccioc,
        'hviol': hviol,
        'hciol': hciol,
        'hccpiolp': hccpiolp,
        'hccpiolh': hccpiolh,
        'eandg': eandg,
        'vvios': vvios,
        'viol': viol,
        'vtios': vtios,
        'tciol': tciol,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render (request, 'process/pro_detail.html', context)
