from django import forms
from django.forms import widgets
from .models import Compound, ElementAll
from django.contrib.auth import get_user_model

class ElementSearchForm(forms.ModelForm):
    class Meta:
        model = ElementAll
        fields = ['compound','name', 'element']
        widgets = {
            'compound':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'id':'myInput','type':'text', 'name':'query','class':'form-control','placeholder':'Name of Compound'}),
            'element':forms.Select(attrs={'class':'form-control'}),
        }