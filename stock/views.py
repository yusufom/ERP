from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from .models import Location, Stock, StockLog, Category
from .forms import LocationCreateForm, StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm, StockLogSearchForm, CategoryCreateForm, StockListSearchForm
from django.http import HttpResponse
import csv
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from employee.models import Employee
from dashboard.models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/erp/')
def list_item(request):
    title = 'List of Items'
    queryset = Stock.objects.all().order_by('id')
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator = Paginator(queryset, 50)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    form = StockSearchForm(request.POST or None)
    if request.method == 'POST':
        category = form['category'].value()
        location = form['location'].value()
        queryset = Stock.objects.filter(
									item_name__icontains=form['item_name'].value(),
                                    condition__icontains=form['condition'].value()
									)
        if (category != ''):
            queryset = queryset.filter(category_id=category)
        
        if (location != ''):
            queryset = queryset.filter(location_id=location)
            
        if form['export_to_EXCEL'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request, "stock/list_item.html", context)

@login_required(login_url='/erp/')
def add_items(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        item_name = form.cleaned_data['item_name']
        q = form.cleaned_data['quantity']
        action  =   f'{request.user.last_name} {request.user.first_name} added {q} {item_name} to the store'
        StockLog.objects.create(action=action, action_by=request.user, datefield=datetime.now())
        messages.success(request, f'{q} {item_name} has been added to the store successfully', extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('stock:add_items')
    context = {
        "form": form,
        "title": "Add Item",
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def update_items(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            location = form.cleaned_data['location']
            item_name = form.cleaned_data['item_name']
            category = form.cleaned_data['category']
            unit = form.cleaned_data['unit']
            condition = form.cleaned_data['condition']
            action  =   f'{request.user.last_name} {request.user.first_name} updated {item_name}\nNew info: Location = {location}, Category = {category}, unit = {unit}, condition = {condition}'
            StockLog.objects.create(action=action, action_by=request.user, datefield=timezone.now())
            messages.success(request, 'Successfully updated', extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('stock:stock_detail',str(queryset.id))
    context = {
        'form':form,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
            }
    return render(request, 'stock/add_items.html', context)

@login_required(login_url='/erp/')
def delete_items(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    title   =   "Delete Item"
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        action  =   f'{request.user.last_name} {request.user.first_name} removed {queryset.item_name} from the store'
        StockLog.objects.create(action=action, action_by=request.user, datefield=datetime.now())
        messages.success(request, 'Successfully Deleted', extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('stock:list_item')
    context = {
        "title": title,
        "queryset": queryset,
        'employeep':employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, 'stock/delete_items.html', context)

@login_required(login_url='/erp/')
def stock_detail(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/stock_detail.html", context)

@login_required(login_url='/erp/')
def issue_items(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    queryset = Stock.objects.get(id=pk)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        ist = form.cleaned_data['issue_quantity']
        to = form.cleaned_data['issue_to']
        un = queryset.unit
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, f'{ist} {un} of {instance.item_name} Issued to {to}. {instance.quantity} {instance.item_name} now left in Store', extra_tags = 'alert alert-success alert-dismissible show')
        instance.save()
        action  =   f'{request.user.last_name} {request.user.first_name} issued out {ist} {un} of {queryset.item_name} to {to}'
        StockLog.objects.create(action=action, action_by=request.user, datefield=datetime.now())
        return redirect('stock:stock_detail',str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def receive_items(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    queryset = Stock.objects.get(id=pk)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        rec = form.cleaned_data['receive_quantity']
        ref = form.cleaned_data['receive_from']
        un = queryset.unit
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        action  =   f'{request.user.last_name} {request.user.first_name} recieved {rec} {un} of {queryset.item_name} from {ref}'
        StockLog.objects.create(action=action, action_by=request.user, datefield=datetime.now())
        messages.success(request, f'{rec} {un} of {instance.item_name} received from {ref}. {instance.quantity} {instance.item_name} now in Store', extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('stock:stock_detail', str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Reaceive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
		}
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def reorder_level(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    queryset = Stock.objects.get(id=pk)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))
        return redirect('stock:stock_detail', str(queryset.id))
    context = {
        "instance": queryset,
        "form": form,
        "title": 'Set Reorder Level',
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
		}
    
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def list_history(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    header = 'STOCK LOG'
    queryset = StockLog.objects.all()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    form = StockLogSearchForm(request.POST or None)
    if request.method == 'POST':
        queryset = StockLog.objects.filter(
                datefield__range=[
                                        form['start_date'].value(),
                                        form['end_date'].value()
                                    ]
                )
            
    
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock Log.csv"'
            writer = csv.writer(response)
            writer.writerow(
				[
				'ACTION',
				'ACTION BY', 
				'TIMESTAMP'])
            instance = queryset
            for stock in instance:
                writer.writerow(
				[ 
				stock.action, 
				stock.action_by, 
				stock.datefield])
            return response
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/list_history.html",context)

@login_required(login_url='/erp/')
def add_category(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    cat = Category.objects.all()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New Category has been added successfully')
        return redirect('stock:add_category')
    context = {
        "form": form,
        "title": "Add Category",
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def add_location(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    loc = Location.objects.all()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = LocationCreateForm(request.POST or None)
    if form.is_valid():
        loc_name = form.cleaned_data['name']
        form.save()
        messages.success(request, f'New Location {loc_name} has been added successfully', extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('stock:add_location')
    context = {
        "form": form,
        "title": "Add Location",
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
	}
    return render(request, "stock/add_items.html", context)

@login_required(login_url='/erp/')
def cat_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    title = 'List of Category'
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    cat = Category.objects.all()
    context = {
        "title": title,
        "cat": cat,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request, "stock/category_list.html", context)

@login_required(login_url='/erp/')
def loc_list(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    title = 'List of Location'
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    loc = Location.objects.all()
    context = {
        "title": title,
        "loc": loc,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request, "stock/location_list.html", context)

@login_required(login_url='/erp/')
def stocklist_cat(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    title = 'List of Category'
    cat = Category.objects.get(id=pk)
    stk = cat.stocks.all()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = StockListSearchForm(request.POST or None)
    if request.method == 'POST':
        stk = Stock.objects.filter(
            item_name__icontains=form['item_name'].value(),
            condition__icontains=form['condition'].value()              
									)
        
        if form['export_to_EXCEL'].value() == True:
            cat = Category.objects.get(id=pk)
            stk = cat.stocks.all()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = stk
            for stock in instance:
                writer.writerow([cat.name, stock.item_name, stock.quantity])
            return response
    context = {
        "title": title,
        "cat": cat,
        'stk': stk,
        'form': form,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request, "stock/stocklist_cat.html", context)

@login_required(login_url='/erp/')
def stocklist_loc(request, pk):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    title = 'List of Location'
    loc = Location.objects.get(id=pk)
    lo = loc.stocks.all()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    form = StockListSearchForm(request.POST or None)
    if request.method == 'POST':
        lo = Stock.objects.filter(
            item_name__icontains=form['item_name'].value(),
            condition__icontains=form['condition'].value()              
									)
        
        
        if form['export_to_EXCEL'].value() == True:
            loc = Location.objects.get(id=pk)
            lo = loc.stocks.all()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['LOCATION', 'ITEM NAME', 'QUANTITY'])
            instance = loc
            for stock in instance:
                writer.writerow([loc.name, stock.item_name, stock.quantity])
            return response
    context = {
        "title": title,
        "loc": loc,
        'lo': lo,
        'form': form,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        }
    return render(request, "stock/stocklist_loc.html", context)