from django import forms
from .models import todo
from employee.models import Payroll, Employee

class TaskupdateForm(forms.ModelForm):
    duedate = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    class Meta:
        model = todo
        fields = ['title', 'description', 'duedate' ,'complete']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'complete':forms.CheckboxInput(),
        }

class PayrollSearchForm(forms.ModelForm):
    export_to_EXCEL = forms.BooleanField(label='Export Schedule', required=False)
    class Meta:
        model = Payroll
        fields = ['employ','month', 'Year']
        widgets = {
            'month':forms.Select(attrs={'class':'form-control'}),
            'Year':forms.Select(attrs={'class':'form-control'}),
            'employ':forms.Select(attrs={'class':'form-control'}),
        }