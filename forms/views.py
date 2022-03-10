import csv
from django.core.paginator import Paginator
from django.http.response import BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import Purchaseorder, Ordersummary, RFsummary, RequestForm
from .forms import POSearchForm, PurchaseorderForm, OrdersummaryFormset, RFsummaryFormset, RequestformForm
import datetime
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa
from django.db.models import Sum
from accounts.models import User
from employee.models import Employee
import os
from django.contrib import messages
from dashboard.models import todo
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required(login_url='/erp/')
def createPO(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    formset = OrdersummaryFormset()
    form = PurchaseorderForm()
    if request.method == 'POST':
        formset = OrdersummaryFormset(request.POST)
        form = PurchaseorderForm(request.POST)
        
        if form.is_valid:
            instance = form.save(commit = False)
            
            approved = request.POST.get('approval')
            assigned_user = User.objects.get(id = approved)
            
            instance.approval = assigned_user
            
            instance.user = request.user
            purchaseorder = Purchaseorder.objects.create(
                user = request.user,
                approval = assigned_user,
                order_to=form.data["order_to"],
                ship_to=form.data["ship_to"],
                payment_terms = form.data["payment_terms"],
                delivery_date=form.data["delivery_date"],
                freight=form.data["freight"], 
                remarks=form.data["remarks"],
                Vatchoice = form.data["Vatchoice"]
                    
                    )
            
            x = datetime.now()
            date= f'{x.day}{x.month}{x.year}'
        if formset.is_valid():
            freights = instance.freight
            total = 0
            for form in formset:
                item_description = form.cleaned_data.get('item_description')
                project = form.cleaned_data.get('project')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if item_description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    if purchaseorder.Vatchoice == 'Exclusive':
                        vat = 0
                    else:
                        vat = 0.075 * float(total)
                    ftotal = float(total) + float(vat) + float(freights)
                    Ordersummary(po=purchaseorder,
                            project=project,
                            item_description=item_description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            purchaseorder.order_no= f'CLPO/{date}/{purchaseorder.id:05d}'
            purchaseorder.subtotal = round(total, 2)
            purchaseorder.VAT= round(vat, 2)
            purchaseorder.total = round(ftotal, 2) 
            purchaseorder.save()
            messages.success(request,f'Purchase Order successfully created.', extra_tags = 'alert alert-success alert-dismissible show')
            
            connection = get_connection() # uses SMTP server specified in settings.py
            connection.open()
            
            Rname   = instance.approval.get_full_name
            Sname   = instance.user.get_full_name
            rmail = instance.approval.email
            subject	=	'PURCHASE ORDER'
            message =	f'Hello {Rname}, {Sname} just created a purchase order. Kindly check by clicking http://cozymltd.com/erp/dashboard/po/view-po/'
            try:
                send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [rmail], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('forms:createPO')
    context = {
        "title" : "Create Purchase Order",
        "formset": formset,
        "form": form,
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request, 'forms/createinvoice.html', context)

@login_required(login_url='/erp/')
def view_PO(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    polist = Purchaseorder.objects.filter(user = user)
    approvalist = Purchaseorder.objects.filter(approval = user)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    
    paginator_po = Paginator(polist, 30)
    page = request.GET.get('page')
    po_paginated = paginator_po.get_page(page)
    
    paginator_ap = Paginator(approvalist, 30)
    page = request.GET.get('page')
    ap_paginated = paginator_ap.get_page(page)
    form = POSearchForm(request.POST or None)
    if request.method == 'POST':
        ap_paginated = Purchaseorder.objects.filter(
                order_no__icontains=form['order_no'].value(),
                created__range=[
                                        form['start_date'].value(),
                                        form['end_date'].value()
                                    ]
                )
    context = {
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'header': 'My Purchase Order',
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now, 
        'polist': po_paginated, 
        'approvalist': ap_paginated,
        'form': form,  
    }
    return render(request, 'forms/view_po.html', context)

@login_required(login_url='/erp/')
def view_one(request, id=None):
    user = request.user
    purs = get_object_or_404(Purchaseorder, id=id)
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    ord 	=	Ordersummary.objects.filter(po_id=id)
    approvalist = Purchaseorder.objects.filter(approval = user)
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    a = purs.approval
    u = purs.user
    a = purs.approval
    x = purs.created
    date= f'{x.day}/{x.month}/{x.year}'
    
    subtotal = round(float(purs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    freight = round(float(purs.freight), 2)
    freightd = f'{float(freight):,}'
    vat = round(float(purs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(purs.total), 2)
    totald = f'{float(total):,}'
    context = {
        'bro': 'Adeleke',
        'purs': purs,
        'ord': ord,
        'approvalist':approvalist,
        'a':a,
        'date': date,
        'u': u,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald,
        'freightd': freightd,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
    }
    return render (request, 'forms/po.html', context)
def fetch_resources(url, rel):
    path = os.path.join(url.replace(settings.STATIC_URL, ""))
    return path

@login_required(login_url='/erp/')
def render_pdf_view(request, id=None):
    ord 	=	Ordersummary.objects.filter(po_id=id)
    user = request.user
    purs = get_object_or_404(Purchaseorder, id=id)
    u = purs.user
    a = purs.approval
    x = purs.created
    date= f'{x.day}/{x.month}/{x.year}'
    approvalist = Purchaseorder.objects.filter(approval = user)
    subtotal = round(float(purs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    freight = round(float(purs.freight), 2)
    freightd = f'{float(freight):,}'
    vat = round(float(purs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(purs.total), 2)
    totald = f'{float(total):,}'
    template_path = 'forms/po_pdf.html'
    context = {
        'purs': purs,
        'ord': ord,
        'myvar': 'this is your template context',
        'approvalist': approvalist,
        'a':a,
        'date': date,
        'u': u,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald,
        'freightd': freightd,
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="PurchaseOrder.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='/erp/')
def download_pdf_view(request, id=None):
    ord 	=	Ordersummary.objects.filter(po_id=id)
    user = request.user
    purs = get_object_or_404(Purchaseorder, id=id)
    u = purs.user
    a = purs.approval
    x = purs.created
    date= f'{x.day}/{x.month}/{x.year}'
    approvalist = Purchaseorder.objects.filter(approval = user)
    subtotal = round(float(purs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    freight = round(float(purs.freight), 2)
    freightd = f'{float(freight):,}'
    vat = round(float(purs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(purs.total), 2)
    totald = f'{float(total):,}'
    template_path = 'forms/po_pdf.html'
    context = {
        'purs': purs,
        'ord': ord,
        'myvar': 'this is your template context',
        'approvalist': approvalist,
        'a':a,
        'date': date,
        'u': u,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald,
        'freightd': freightd,
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PurchaseOrder.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='/erp/')
def approve_PO(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
    po = get_object_or_404(Purchaseorder, id = id)
    x = datetime.now()
    date= f'{x.day}/{x.month}/{x.year}'
    po.mdate = date
    po.approve_po
    po.save
    
    connection = get_connection() # uses SMTP server specified in settings.py
    connection.open()
    Rname   = po.approval.get_full_name
    Sname   = po.user.get_full_name
    rmail = po.approval.email
    smail = po.user.get_full_name
    subject	=	'PURCHASE ORDER'
    message =	f'Hello {Sname}, {Rname} just approved your purchase order \n Purchase order no : {po.order_no} \n Date Created: {po.created}'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [smail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    messages.success(request,f'Purchase order {po.order_no} successfully approved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewPONE', id = id)

@login_required(login_url='/erp/')
def unapprove_PO(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
    po = get_object_or_404(Purchaseorder, id = id)
    po.unapprove_po
    
    connection = get_connection() # uses SMTP server specified in settings.py
    connection.open()
    Rname   = po.approval.get_full_name
    Sname   = po.user.get_full_name
    rmail = po.approval.email
    smail = po.user.get_full_name
    subject	=	'PURCHASE ORDER'
    message =	f'Hello {Sname}, {Rname} just unapproved your purchase order \n Purchase order no : {po.order_no} \n Date Created: {po.created}'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [smail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    
    messages.success(request,f'Purchase order {po.order_no} successfully unapproved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewPONE', id = id) 

@login_required(login_url='/erp/')
def reject_PO(request,id):
    if not request.user.is_authenticated:
        return redirect('/')
    po = get_object_or_404(Purchaseorder, id = id)
    po.reject_po
    
    connection = get_connection() # uses SMTP server specified in settings.py
    connection.open()
    Rname   = po.approval.get_full_name
    Sname   = po.user.get_full_name
    rmail = po.approval.email
    smail = po.user.get_full_name
    subject	=	'PURCHASE ORDER'
    message =	f'Hello {Sname}, {Rname} just rejected your purchase order \n Purchase order no : {po.order_no} \n Date Created: {po.created}'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [smail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,'Purchase order has been rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewPONE', id = id)

@login_required(login_url='/erp/')
def unreject_PO(request,id):
    po = get_object_or_404(Purchaseorder, id = id)
    po.status = 'Pending'
    po.is_approved = False
    po.save()
    messages.success(request,'Purchase Order has been unrejected ',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewPONE', id = id)

@login_required(login_url='/erp/')
def createRF(request):
    user = request.user
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    formset = RFsummaryFormset()
    form = RequestformForm()
    if request.method == 'POST':
        formset = RFsummaryFormset(request.POST)
        form = RequestformForm(request.POST)
        
        if form.is_valid:
            instance = form.save(commit = False)
            
            Mapproved = request.POST.get('Manager_approval')
            assigned_user = User.objects.get(id = Mapproved)
            
            instance.rfapproval = assigned_user
            
            FMapproved = request.POST.get('Finance_approval')
            assigned_userf = User.objects.get(id = FMapproved)
            
            instance.fmapproved = assigned_userf
            
            instance.user = request.user
            requestform = RequestForm.objects.create(
                user = request.user,
                Manager_approval = assigned_user,
                Finance_approval = assigned_userf,
                currency=form.data["currency"],
                comment=form.data["comment"],
                Vatchoice = form.data["Vatchoice"],
                pmode=form.data["pmode"],
                beneficiary=form.data["beneficiary"], 
                bacctinfo=form.data["bacctinfo"],
                others = form.data["others"],
                rdetails = form.data["rdetails"]
                    
                    )
            
            x = datetime.now()
            date= f'{x.day}{x.month}{x.year}'
        if formset.is_valid():
            total = 0
            for form in formset:
                item_description = form.cleaned_data.get('item_description')
                project = form.cleaned_data.get('project')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if item_description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    if requestform.Vatchoice == 'Exclusive':
                        vat = 0
                    else:
                        vat = 0.075 * float(total)
                    ftotal = float(total) + float(vat)
                    RFsummary(rf=requestform,
                            project=project,
                            item_description=item_description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            requestform.cctr= f'{requestform.id:05d}'
            requestform.subtotal = round(total, 2)
            requestform.VAT= round(vat, 2)
            requestform.total = round(ftotal, 2) 
            requestform.save()
            
            connection = get_connection() 
            connection.open()
            Rname   = instance.rfapproval.get_full_name
            Sname   = instance.fmapproved.get_full_name
            Uname   =  instance.user.get_full_name
            rmail   = instance.rfapproval.email
            smail   = instance.fmapproved
            umail   = instance.user.get_full_name
            subject	=	'REQUEST FORM'
            message =	f'Hello {Rname}, {Uname} just created a request form and is awaiting your approval. Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
            try:
                send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [rmail], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            return redirect('forms:createRF')
            
            
        
    context = {
        "title" : "Create Request Form",
        "formset": formset,
        "form": form,
        'employeep': employeep,
        'employees_birthday': employees_birthday,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
    }
    return render(request, 'forms/createrf.html', context)

class view_RF(LoginRequiredMixin, View):
    login_url='/erp/'
    
    def get(self, *arg, **kwargs):
        user = self.request.user
        employeep = Employee.objects.filter(user = user).first()
        employees_birthday = Employee.objects.birthdays_current_month()
        rflist = RequestForm.objects.filter(user = user)
        approvalist = RequestForm.objects.filter(Manager_approval = user)
        Fapprovalist = RequestForm.objects.filter(Finance_approval = user)
        tasks = todo.objects.filter(user=user)
        tasklist = tasks.order_by('complete','duedate')
        count = todo.objects.filter(complete=False).count()
        now = datetime.date(datetime.now())
        
        paginator_rf = Paginator(rflist, 30)
        page = self.request.GET.get('page')
        po_paginated = paginator_rf.get_page(page)
        
        paginator_ap = Paginator(approvalist, 30)
        page = self.request.GET.get('page')
        ap_paginated = paginator_ap.get_page(page)
        
        paginator_fap = Paginator(Fapprovalist, 30)
        page = self.request.GET.get('page')
        fap_paginated = paginator_fap.get_page(page)
        context = {
            'employees_birthday': employees_birthday,
            'employeep': employeep,
            'header': 'My Requisition Forms',
            'tasklist': tasklist,
            'count': count,
            'tasks': tasks,
            'now': now,
            'rflist': po_paginated, 
            'approvalist': ap_paginated,
            'Fapprovalist': fap_paginated,
            
        }
        return render(self.request, 'forms/view_rf.html', context)
    def post(self, request):        
        rf_ids = request.POST.getlist("rf_id")
        rf_ids = list(map(int, rf_ids))

        update_status_for_invoices = int(request.POST['status'])
        rfz = RequestForm.objects.filter(id__in=rf_ids)
        if update_status_for_invoices == 0:
            rfz.update(pstatus=False)
        else:
            rfz.update(pstatus=True)

        return redirect('forms:viewRF')

def change_status(request):
    return redirect('forms:viewRF')

@login_required(login_url='/erp/')
def view_onerf(request, id=None):
    user = request.user
    rfs = get_object_or_404(RequestForm, id=id)
    rfsd 	=	RFsummary.objects.filter(rf_id=id)
    approvaM = RequestForm.objects.filter(Manager_approval = user)
    approvaFM = RequestForm.objects.filter(Finance_approval = user)
    employeep = Employee.objects.filter(user = user).first()
    employees_birthday = Employee.objects.birthdays_current_month()
    tasks = todo.objects.filter(user=user)
    tasklist = tasks.order_by('complete','duedate')
    count = todo.objects.filter(complete=False).count()
    now = datetime.date(datetime.now())
    a = rfs.Manager_approval
    u = rfs.user
    f = rfs.Finance_approval
    x = rfs.created
    subtotal = round(float(rfs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    vat = round(float(rfs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(rfs.total), 2)
    totald = f'{float(total):,}'
    date= f'{x.day}/{x.month}/{x.year}'
    context = {
        'rfs': rfs,
        'rfsd': rfsd,
        'approvaM':approvaM,
        'a':a,
        'date': date,
        'u': u,
        'f':f,
        'approvaFM': approvaFM,
        'tasklist': tasklist,
        'count': count,
        'tasks': tasks,
        'now': now,
        'employees_birthday': employees_birthday,
        'employeep': employeep,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald
    }
    return render (request, 'forms/requestform.html', context)

@login_required(login_url='/erp/')
def rfrender_pdf_view(request, id=None):
    rfsd 	=	RFsummary.objects.filter(rf_id=id)
    user = request.user
    rfs = get_object_or_404(RequestForm, id=id)
    approvaM = RequestForm.objects.filter(Manager_approval = user)
    approvaFM = RequestForm.objects.filter(Finance_approval = user)
    a = rfs.Manager_approval
    u = rfs.user
    f = rfs.Finance_approval
    x = rfs.created
    date= f'{x.day}/{x.month}/{x.year}'
    subtotal = round(float(rfs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    vat = round(float(rfs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(rfs.total), 2)
    totald = f'{float(total):,}'
    template_path = 'forms/requestPDF.html'
    context = {
        'rfs': rfs,
        'rfsd': rfsd,
        'approvaM':approvaM,
        'a':a,
        'date': date,
        'u': u,
        'f':f,
        'approvaFM': approvaFM,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Requestform.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='/erp/')
def rfdownload_pdf_view(request, id=None):
    rfsd 	=	RFsummary.objects.filter(rf_id=id)
    user = request.user
    rfs = get_object_or_404(RequestForm, id=id)
    approvaM = RequestForm.objects.filter(Manager_approval = user)
    approvaFM = RequestForm.objects.filter(Finance_approval = user)
    a = rfs.Manager_approval
    u = rfs.user
    f = rfs.Finance_approval
    x = rfs.created
    date= f'{x.day}/{x.month}/{x.year}'
    subtotal = round(float(rfs.subtotal), 2)
    subtotald = f'{float(subtotal):,}'
    vat = round(float(rfs.VAT), 2)
    vatd = f'{float(vat):,}'
    total = round(float(rfs.total), 2)
    totald = f'{float(total):,}'
    template_path = 'forms/requestPDF.html'
    context = {
        'rfs': rfs,
        'rfsd': rfsd,
        'approvaM':approvaM,
        'a':a,
        'date': date,
        'u': u,
        'f':f,
        'approvaFM': approvaFM,
        'subtotald': subtotald,
        'vatd': vatd,
        'totald': totald
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Requestform.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='/erp/')
def approve_RF(request,id):
    rfs = get_object_or_404(RequestForm, id=id)
    if not request.user.is_authenticated:
        return redirect('/erp/')
    x = datetime.now()
    mdate= f'{x.day}/{x.month}/{x.year}'
    rf = get_object_or_404(RequestForm, id = id)
    rf.mdate = mdate
    rf.approve_rf
    rf.save()
    
    connection = get_connection() 
    connection.open()
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Sname}, {Rname} just approved the request form created by {Uname} and is awaiting your final approval. \n Request Form No: {rf.cctr} \n Created on: {rf.created} \n Amount: {rfs.total} \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [smail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    messages.success(request,f'Request Form {rf.cctr} successfully approved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def fapprove_RF(request,id):
    if not request.user.is_authenticated:
        return redirect('/erp/')
    x = datetime.now()
    fdate= f'{x.day}/{x.month}/{x.year}'
    rf = get_object_or_404(RequestForm, id = id)
    rf.fdate = fdate
    rf.fmapprove_rf
    rf.save()
    
    connection = get_connection() 
    connection.open()
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Uname}, your request form has received its final approval \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [umail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,f'Request Form {rf.cctr} successfully approved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def unapprove_RF(request,id):
    if not request.user.is_authenticated:
        return redirect('/erp/')
    rf = get_object_or_404(RequestForm, id = id)
    rf.unapprove_rf
    
    connection = get_connection() 
    connection.open()
    
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Uname}, your request form has been unapproved by your manager. \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [umail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,f'Request Form {rf.cctr} successfully unapproved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id) 

@login_required(login_url='/erp/')
def funapprove_RF(request,id):
    if not request.user.is_authenticated:
        return redirect('/erp/')
    rf = get_object_or_404(RequestForm, id = id)
    rf.fmunapprove_rf
    
    connection = get_connection() 
    connection.open()
    
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Uname}, your request form has been unapproved by Finance Manager. \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [umail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,f'Request Form {rf.cctr} successfully unapproved.', extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def reject_RF(request,id):
    if not request.user.is_authenticated:
        return redirect('/erp/')
    rf = get_object_or_404(RequestForm, id = id)
    rf.reject_rf
    
    connection = get_connection() 
    connection.open()
    
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Uname}, your request form has been rejected by your Manager. \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [umail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,'Request Form has been rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def freject_RF(request,id):
    if not request.user.is_authenticated:
        return redirect('/erp/')
    rf = get_object_or_404(RequestForm, id = id)
    rf.fmreject_rf
    
    connection = get_connection() 
    connection.open()
    
    Rname   = rf.rfapproval.get_full_name
    Sname   = rf.fmapproved.get_full_name
    Uname   =  rf.user.get_full_name
    rmail   = rf.rfapproval.email
    smail   = rf.fmapproved
    umail   = rf.user.get_full_name
    subject	=	'REQUEST FORM'
    message =	f'Hello {Uname}, your request form has been rejected by the Finance Manager. \n Kindly check by clicking http://cozymltd.com/erp/dashboard/rf/view-rf/'
    try:
        send_mail(subject, message, ['olamilekan.yusuf@cozymltd.com'], [umail], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    
    messages.success(request,'Request Form has been rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def unreject_RF(request,id):
    rf = get_object_or_404(RequestForm, id = id)
    rf.status = 'Pending'
    rf.is_approved = False
    rf.save()
    messages.success(request,'Request Form has been unrejected ',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)

@login_required(login_url='/erp/')
def funreject_RF(request,id):
    rf = get_object_or_404(RequestForm, id = id)
    rf.fstatus = 'Pending'
    rf.is_fapproved = False
    rf.save()
    messages.success(request,'Request Form has been unrejected ',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('forms:viewRFONE', id = id)