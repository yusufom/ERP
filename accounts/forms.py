from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    
class UserAddForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'First name.First Letter of last name e.g Olamilekan.Y'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'type':'email','class':'form-control','placeholder':'Email: eg.olamilekan.yusuf@cozymltd.com'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter the same password as before, for verification.'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2',]
        
    def clean_email(self):
        email = self.cleaned_data['email']
        qry = User.objects.filter(email = email)
        
        domain_list = ['cozymltd.com']
        get_cozym_domain = email.split('@')[1]#get me whatever after @, eg. gmail.com
        
        print(get_cozym_domain in domain_list)
        
        if qry.exists():
            raise forms.ValidationError('email {0} already exists'.format(email))
        
        elif get_cozym_domain not in domain_list:
            print('test - not in domain')
            raise forms.ValidationError("email does not contain company's domain name")
        
        return email