from django import forms
from employee.models import Department,Bank,Emergency, Payroll,Relationship,Employee
from django.conf import settings


User=settings.AUTH_USER_MODEL

# EMPLoYEE
class EmployeeCreateForm(forms.ModelForm):
    RELIGION = (
        ('Islam','Islam'),
    ('Christianity','Christianity'),
    ('OTHER','Other'),
    )
    
    GENDER = (
    ('MALE','Male'),
    ('FEMALE','Female'),
    ('OTHER','Other'),
    ('NOT_KNOWN','Not Known'),
    )

    TITLE = (
    ('MR','Mr'),
    ('MRS','Mrs'),
    ('MISS','Miss'),
    ('DR','Dr'),
    ('SIR','Sir'),
    ('MADAM','Madam'),
    )

    EMPLOYEETYPE = (
    ('Full Time','Full-Time'),
    ('Part Time','Part-Time'),
    ('Contract','Contract'),
    ('Intern','Intern'),
    )
    
    EDUCATIONAL_LEVEL = (
    ('SENIORHIGH','Senior High School'),
    ('JUNIORHIGH','Junior High School'),
    ('PRIMARY','Primary School'),
    ('TERTIARY','Tertiary/University/Polytechnic'),
    ('OLEVEL','OLevel'),
    ('OTHER','Other'),
    )
    title = forms.ChoiceField(label='Title', widget=forms.Select(attrs={'class':'form-control'}), choices = TITLE)
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'onchange':'previewImage(this);', 'class':'form-control'}))
    firstname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Surname'}))
    othername = forms.CharField(required=False, label='Other Name (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Other Name'}))
    sex = forms.ChoiceField(label='Gender', widget=forms.Select(attrs={'class':'form-control', }), choices = GENDER)
    tel = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'+234'}))
    birthday = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control','placeholder':'2021-12-23'}))
    religion = forms.ChoiceField(label='Religion', widget=forms.Select(attrs={'class':'form-control'}), choices = RELIGION)
    hometown = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State of Origin'}))
    residence = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current City'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current Address'}))
    education = forms.ChoiceField(label='Highest Education Received', widget=forms.Select(attrs={'class':'form-control', }), choices = EDUCATIONAL_LEVEL)
    lastwork = forms.CharField(required=False, label='Last Place of Work', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last place of work of employee'}))
    position = forms.CharField(required=False, label='Position Held', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Employees position at last place of work'}))
    ssnitnumber = forms.CharField(required=False, label='NSIT (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'NSIT'}))
    tinnumber = forms.CharField(required=False, label='TIN number (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'TIN'}))
    role = forms.CharField(label='Current position', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current Position in the Company'}))
    startdate = forms.DateField(label='Date of Commencement', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    employeetype = forms.ChoiceField(label='Employment Type', widget=forms.Select(attrs={'class':'form-control'}), choices = EMPLOYEETYPE)
    employeeid = forms.CharField(label='Employee Code',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'e.g For Engineering (EG001)'}))
    dateissued = forms.DateField(label='Date Issued', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    
    class Meta:
        model = Employee
        exclude = ['is_blocked','is_deleted','created','updated', 'email']
        widgets = {
            'user': forms.Select(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell us a little bit about yourself'}),
            'nationality':forms.TextInput(attrs={'class':'form-control','placeholder':'Nationality'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            
		}
        
    def clean_user(self):
        user = self.cleaned_data['user'] #returns <User object>,not id as in [views <-> templates]
        qry = Employee.objects.filter(user = user)#check, whether any employee exist with username - avoid duplicate users - > many employees
        if qry:
            raise forms.ValidationError('Employee exists with username already')
        return user

class EmployeeEditForm(forms.ModelForm):
    RELIGION = (
        ('Islam','Islam'),
    ('Christianity','Christianity'),
    ('OTHER','Other'),
    )
    
    GENDER = (
    ('MALE','Male'),
    ('FEMALE','Female'),
    ('OTHER','Other'),
    ('NOT_KNOWN','Not Known'),
    )

    TITLE = (
    ('MR','Mr'),
    ('MRS','Mrs'),
    ('MISS','Miss'),
    ('DR','Dr'),
    ('SIR','Sir'),
    ('MADAM','Madam'),
    )

    EMPLOYEETYPE = (
    ('Full Time','Full-Time'),
    ('Part Time','Part-Time'),
    ('Contract','Contract'),
    ('Intern','Intern'),
    )
    
    EDUCATIONAL_LEVEL = (
    ('SENIORHIGH','Senior High School'),
    ('JUNIORHIGH','Junior High School'),
    ('PRIMARY','Primary School'),
    ('TERTIARY','Tertiary/University/Polytechnic'),
    ('OLEVEL','OLevel'),
    ('OTHER','Other'),
    )
    title = forms.ChoiceField(label='Title', widget=forms.Select(attrs={'class':'form-control'}), choices = TITLE)
    firstname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Surname'}))
    othername = forms.CharField(required=False, label='Other Name (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Other Name'}))
    sex = forms.ChoiceField(label='Gender', widget=forms.Select(attrs={'class':'form-control', }), choices = GENDER)
    tel = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'+234'}))
    birthday = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control','placeholder':'2021-12-23'}))
    religion = forms.ChoiceField(label='Religion', widget=forms.Select(attrs={'class':'form-control'}), choices = RELIGION)
    hometown = forms.CharField(required=False, label='State', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State of Origin'}))
    residence = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current City'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current Address'}))
    education = forms.ChoiceField(label='Highest Education Received', widget=forms.Select(attrs={'class':'form-control', }), choices = EDUCATIONAL_LEVEL)
    lastwork = forms.CharField(required=False, label='Last Place of Work', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last place of work of employee'}))
    position = forms.CharField(required=False, label='Position Held', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Employees position at last place of work'}))
    ssnitnumber = forms.CharField(required=False, label='NSIT (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'NSIT'}))
    tinnumber = forms.CharField(required=False, label='TIN number (Optional)', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'TIN'}))
    role = forms.CharField(label='Current position', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Current Position in the Company'}))
    startdate = forms.DateField(label='Date of Commencement', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    employeetype = forms.ChoiceField(label='Employment Type', widget=forms.Select(attrs={'class':'form-control'}), choices = EMPLOYEETYPE)
    
    class Meta:
        model = Employee
        exclude = ['user', 'image', 'is_blocked','is_deleted','created','updated', 'email', 'employeeid', 'dateissued' ]
        widgets = {
            'bio':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell us a little bit about yourself'}),
            'nationality':forms.TextInput(attrs={'class':'form-control','placeholder':'Nationality'}),
            'department':forms.Select(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
		}




class EmergencyCreateForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['employee','fullname','tel','location','relationship']
        widgets = {
            'employee':forms.Select(attrs={'class':'form-control'}),
            'fullname':forms.TextInput(attrs={'class':'form-control'}),
            'tel':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'relationship':forms.Select(attrs={'class':'form-control'})
        }





# FAMILY

class FamilyCreateForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ['employee','status','spouse','occupation','tel','children','nextofkin','contact','relationship','father','foccupation','mother','moccupation']
        widgets = {
            'employee':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'spouse':forms.TextInput(attrs={'class':'form-control'}),
            'occupation':forms.TextInput(attrs={'class':'form-control'}),
            'tel':forms.TextInput(attrs={'class':'form-control'}),
            'children':forms.TextInput(attrs={'class':'form-control'}),
            'nextofkin':forms.TextInput(attrs={'class':'form-control'}),
            'contact':forms.TextInput(attrs={'class':'form-control'}),
            'relationship':forms.Select(attrs={'class':'form-control'}),
            'father':forms.TextInput(attrs={'class':'form-control'}),
            'foccupation':forms.TextInput(attrs={'class':'form-control'}),
            'mother':forms.TextInput(attrs={'class':'form-control'}),
            'moccupation':forms.TextInput(attrs={'class':'form-control'}),
        }



class BankAccountCreation(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['employee','name','branch','account','salary', 'basic', 'housing', 'transport']
        widgets = {
            'employee':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'branch':forms.TextInput(attrs={'class':'form-control'}),
            'account':forms.TextInput(attrs={'class':'form-control'}),
            'salary':forms.TextInput(attrs={'class':'form-control'}),
            'basic':forms.TextInput(attrs={'class':'form-control'}),
            'housing':forms.TextInput(attrs={'class':'form-control'}),
            'transport':forms.TextInput(attrs={'class':'form-control'}),
        }

class PayrollCreationForm(forms.ModelForm):
    paymentdate = forms.DateField(label='Date Issued', widget=forms.DateInput(attrs={'type':"date", 'class':'form-control'}))
    deductther = forms.CharField(label='Other Deductions', widget=forms.TextInput(attrs={'class':'form-control'}), required=False, initial=0)
    class Meta:
        model = Payroll
        fields = ['employ', 'month', 'Year','paymentdate', 'overtime', 'bonus', 'paye', 'deductther', 'loan',]
        widgets = {
            'employ':forms.Select(attrs={'class':'form-control'}),
            'month':forms.Select(attrs={'class':'form-control'}),
            'Year':forms.Select(attrs={'class':'form-control'}),
            'overtime':forms.TextInput(attrs={'class':'form-control'}),
            'paye':forms.TextInput(attrs={'class':'form-control'}),
            'loan':forms.TextInput(attrs={'class':'form-control'}),
            'bonus':forms.TextInput(attrs={'class':'form-control'}),
        }
class DeptCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
        }