from django import forms
from django.forms import formset_factory, widgets
from .models import Purchaseorder, Ordersummary, RFsummary, RequestForm

class PurchaseorderForm(forms.ModelForm):
    order_to = forms.CharField(label='Order To', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Order To','rows':1 }))
    ship_to = forms.CharField(label='Ship To', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ship To','rows':1}))
    payment_terms = forms.CharField(label='Payment Terms', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '','rows':1}))
    delivery_date = forms.DateField(label='Delivery Date', widget=forms.DateInput(attrs={'class': 'form-control input','placeholder': '','rows':1,'type': 'date', 'name':"delivery_date"}))
    freight = forms.IntegerField(label='Freight', widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '','rows':1}))
    remarks = forms.CharField(label='Remarks', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Remarks','rows':1}))
    
    class Meta:
        model = Purchaseorder
        fields = ['approval','order_to', 'ship_to', 'payment_terms', 'delivery_date', 'freight', 'remarks', 'Vatchoice']
        widgets = {
            'Vatchoice':forms.Select(attrs={'class':'form-control'}),
            'approval':forms.Select(attrs={'class':'form-control'}),
        }

class OrdersummaryForm(forms.Form):
    item_description = forms.CharField(label='Description', widget=forms.TextInput(attrs={'class': 'formed input','placeholder': 'Enter Item Description'}))
    project = forms.CharField(label='Project Name', widget=forms.TextInput(attrs={'class': 'formed input','placeholder': 'Project Name'}))
    quantity = forms.IntegerField(label='Quantity', widget=forms.TextInput(attrs={'class': 'formed input quantity','placeholder': 'Quantity'}))
    rate = forms.DecimalField(label='Unit Price', widget=forms.TextInput(attrs={'class': 'formed input rate', 'placeholder': 'Unit Price'}))
    # amount = forms.IntegerField(
    #     label='Total Price',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input quantity',
    #         'placeholder': 'Total Price'
    #     }) #quantity should not be less than one
    # )
    
OrdersummaryFormset = formset_factory(OrdersummaryForm, extra=1)

class POSearchForm(forms.ModelForm):
    order_no = forms.CharField(required=False,label='Order No', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search Order No'}))
    start_date = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    end_date = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    class Meta:
        model = Purchaseorder
        fields = ['order_no','start_date', 'end_date']

class RequestformForm(forms.ModelForm):
    comment = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Comment','rows':3, 'col':3 }))
    beneficiary = forms.CharField(required=False, label='Beneficiary', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Beneficiary','rows':1}))
    bacctinfo = forms.CharField(required=False, label='Beneficiary Account Info', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '','rows':1}))
    others = forms.CharField(required=False, label='Others', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Remarks','rows':1}))
    rdetails = forms.CharField(required=False, label='Refund Details', widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Refund Details','rows':1}))
    
    class Meta:
        model = RequestForm
        fields = ['Manager_approval','Finance_approval','currency', 'comment', 'Vatchoice', 'pmode', 'beneficiary', 'bacctinfo', 'others', 'rdetails']
        widgets = {
            'Vatchoice':forms.Select(attrs={'class':'form-control'}),
            'Manager_approval':forms.Select(attrs={'class':'form-control'}),
            'Finance_approval':forms.Select(attrs={'class':'form-control'}),
            'currency':forms.Select(attrs={'class':'form-control'}),
            'pmode':forms.Select(attrs={'class':'form-control'}),
        }

class RFsummaryForm(forms.Form):
    item_description = forms.CharField(label='Description', widget=forms.TextInput(attrs={'class': 'formed input','placeholder': 'Enter Item Description'}))
    project = forms.CharField(label='Project Name', widget=forms.TextInput(attrs={'class': 'formed input','placeholder': 'Project Name'}))
    quantity = forms.IntegerField(label='Quantity', widget=forms.TextInput(attrs={'class': 'formed input quantity','placeholder': 'Quantity'}))
    rate = forms.DecimalField(label='Unit Price', widget=forms.TextInput(attrs={'class': 'formed input rate', 'placeholder': 'Unit Price'}))
    # amount = forms.IntegerField(
    #     label='Total Price',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input quantity',
    #         'placeholder': 'Total Price'
    #     }) #quantity should not be less than one
    # )
RFsummaryFormset = formset_factory(RFsummaryForm, extra=1)