# Create your models here.
from django.db import models
from .managers import POManager, RFManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.conf import settings

User=settings.AUTH_USER_MODEL


# Create your models here.
class Purchaseorder(models.Model):
    VAT = {
        ('Inclusive','Inclusive'),
        ('Exclusive','Exclusive'),
    }
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='writer')
    approval        = models.ForeignKey(User,on_delete=models.CASCADE,related_name='approver')
    order_to        = models.CharField(max_length=2000, blank=True, null=True)
    order_no        = models.CharField(max_length=2000, blank=True, null=True)
    ship_to         = models.CharField(max_length=2000, blank=True, null=True)
    payment_terms   = models.CharField(max_length=2000, blank=True, null=True)
    delivery_date   = models.DateField(max_length=2000, blank=True, null=True)
    subtotal        = models.CharField(max_length=2000, blank=True, null=True)
    Vatchoice       = models.CharField(max_length=2000, blank=False, null=True, choices=VAT)
    VAT             = models.CharField(max_length=2000, blank=True, null=True)
    freight         = models.CharField(max_length=2000, blank=True, null=True)
    total           = models.CharField(max_length=2000, blank=True, null=True)
    remarks         = models.TextField(max_length=2000, blank=True, null=True)
    created         = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False) 
    status          = models.CharField(max_length=2000, blank=True, null=True, default='Pending')
    mdate           = models.CharField(max_length=2000, blank=True, null=True)
    is_approved     = models.BooleanField(default=False)
    is_rejected     = models.BooleanField(default=False)
    is_cancelled    = models.BooleanField(default=False)
    
    objects = POManager()
    
    class Meta:
        verbose_name = _('Purchaseorder')
        verbose_name_plural = _('Purchaseorders')
        ordering = ['-created'] #recent objects
    
    @property    
    def porder(self):
        p = self.order_no
        user = self.user
        employee = user.employee_set.first().get_full_name
        return ('{0} - {1}'.format(employee,p))
    
    @property
    def po_approved(self):
        return self.is_approved == True
    
    @property
    def approve_po(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'Approved'
            self.save()
            
    @property
    def unapprove_po(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'Pending'
            self.save()
            
    @property
    def reject_po(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'Rejected'
            self.save()
            
    @property
    def is_rejected(self):
        return self.status == 'Rejected'

class  Ordersummary(models.Model):
    po = models.ForeignKey(Purchaseorder, related_name='purchaseorder', blank=True, on_delete=models.CASCADE)
    item_description= models.CharField(max_length=2000, blank=True, null=True)
    project = models.CharField(max_length=2000, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    rate      = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    amount     = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    
class RequestForm(models.Model):
    VAT = {
        ('Inclusive','Inclusive'),
        ('Exclusive','Exclusive'),
    }
    Currency = {
        ('Naira','Naira'),
        ('Dollars','Dollars'),
        ('Pounds Sterling','Pounds Sterling'),
        ('Euro','Euro'),
        ('Bitcoin','Bitcoin'),
        ('Etherum','Etherum')
    }
    PaymentMode = {
        ('Cash','Cash'),
        ('Cheque','Cheque'),
        ('Electronic','Electronic'),
    }
    user            = models.ForeignKey(User,on_delete=models.CASCADE, related_name='rfname')
    Manager_approval= models.ForeignKey(User,on_delete=models.CASCADE,related_name='rfapprover')
    Finance_approval= models.ForeignKey(User,on_delete=models.CASCADE,related_name='fmapprover')
    cctr            = models.CharField(max_length=2000, blank=True, null=True)
    currency        = models.CharField(max_length=2000, blank=False, null=False, choices=Currency)
    comment         = models.TextField(max_length=2000, blank=True, null=True)
    subtotal        = models.CharField(max_length=2000, blank=True, null=True)
    Vatchoice       = models.CharField(max_length=2000, blank=False, null=True, choices=VAT)
    VAT             = models.CharField(max_length=2000, blank=True, null=True)
    total           = models.CharField(max_length=2000, blank=True, null=True)
    pmode           = models.CharField(max_length=2000, blank=False, null=False, choices=PaymentMode)
    beneficiary     = models.CharField(max_length=2000, blank=True, null=True)
    bacctinfo       = models.CharField(max_length=2000, blank=True, null=True)
    others          = models.CharField(max_length=2000, blank=True, null=True)
    mdate           = models.CharField(max_length=2000, blank=True, null=True)
    fdate           = models.CharField(max_length=2000, blank=True, null=True)
    rdetails        = models.CharField(max_length=2000, blank=True, null=True)
    created         = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False) 
    status          = models.CharField(max_length=2000, blank=True, null=True, default='Pending')
    fstatus          = models.CharField(max_length=2000, blank=True, null=True, default='Pending')
    is_approved     = models.BooleanField(default=False)
    is_fapproved     = models.BooleanField(default=False)
    pstatus     = models.BooleanField(default=False)
    
    objects = RFManager()
    
    class Meta:
        verbose_name = _('RequestForm')
        verbose_name_plural = _('RequestForms')
        ordering = ['-created'] #recent objects
    
    def get_status(self):
        return self.pstatus
    
    @property    
    def rf(self):
        r = self.requesting_name
        user = self.user
        employee = user.employee_set.first().get_full_name
        return ('{0} - {1}'.format(employee,r))
    
    @property
    def rf_approved(self):
        return self.is_approved == True
    
    @property
    def rf_fmapproved(self):
        return self.is_fapproved == True
    
    @property
    def approve_rf(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'Approved'
            self.save()
    
    @property
    def fmapprove_rf(self):
        if not self.is_fapproved:
            self.is_fapproved = True
            self.fstatus = 'Approved'
            self.save()
            
    @property
    def unapprove_rf(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'Pending'
            self.save()
            
    @property
    def fmunapprove_rf(self):
        if self.is_fapproved:
            self.is_fapproved = False
            self.fstatus = 'Pending'
            self.save()
            
    @property
    def reject_rf(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'Rejected'
            self.save()
            
    @property
    def fmreject_rf(self):
        if self.is_fapproved or not self.is_fapproved:
            self.is_fapproved = False
            self.fstatus = 'Rejected'
            self.save()
            
    @property
    def is_rejected(self):
        return self.status == 'Rejected'
    
    @property
    def is_frejected(self):
        return self.fstatus == 'Rejected'

class  RFsummary(models.Model):
    rf = models.ForeignKey(RequestForm, related_name='requestform', blank=True, on_delete=models.CASCADE)
    item_description= models.CharField(max_length=2000, blank=True, null=True)
    project = models.CharField(max_length=2000, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    rate      = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    amount     = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)