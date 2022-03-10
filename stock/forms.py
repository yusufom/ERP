from django import forms
from django.forms import widgets
from .models import Location, Stock, StockLog, Category
from django.contrib.auth import get_user_model


class StockSearchForm(forms.ModelForm):
    export_to_EXCEL = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['location','category', 'item_name', 'condition']
        widgets = {
            'location':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'item_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Item'}),
            'condition':forms.Select(attrs={'class':'form-control'}),
        }

class StockListSearchForm(forms.ModelForm):
    export_to_EXCEL = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['item_name', 'condition']
        widgets = {
            'item_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Item'}),
            'condition':forms.Select(attrs={'class':'form-control'}),
        }

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['location','category', 'item_name', 'quantity', 'unit', 'condition', 'comment']
        widgets = {
            'location':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'item_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Item'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'condition':forms.Select(attrs={'class':'form-control'}),
            'comment':forms.Textarea(attrs={'class':'form-control'}),
        }
    
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name
    
class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['location', 'category', 'item_name', 'unit', 'condition']
        widgets = {
            'location':forms.Select(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'item_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Item'}),
            'unit':forms.Select(attrs={'class':'form-control'}),
            'condition':forms.Select(attrs={'class':'form-control'}),
        }
        
class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']
        widgets = {
            'issue_quantity': forms.NumberInput(attrs={'class':'form-control'}),
            'issue_to': forms.TextInput(attrs={'class':'form-control'}),
        }


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'receive_from']
        widgets = {
            'receive_quantity': forms.NumberInput(attrs={'class':'form-control'}),
            'receive_from': forms.TextInput(attrs={'class':'form-control'}),
        }
        
class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
        widgets = {
            'reorder_level': forms.NumberInput(attrs={'class':'form-control'}),
        }

class StockLogSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    start_date = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    end_date = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    class Meta:
        model = StockLog
        fields = ['start_date', 'end_date']   
        
class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Category'})
        }
        
class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of Location'})
        }