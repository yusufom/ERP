import datetime

from django.db.models.enums import Choices
from employee.utility import code_format
from django.db import models
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from leave.models import Leave
from django.conf import settings

User=settings.AUTH_USER_MODEL


# Create your models here.
class Department(models.Model):
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name','created']
    
    def __str__(self):
        return self.name


class Bank(models.Model):
    # access table: employee.bank_set.
    employee = models.ForeignKey('Employee',help_text='select employee(s) to add bank account',on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
    account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
    branch = models.CharField(_('Branch'),help_text='which branch was the account issue',max_length=125,blank=True,null=True)
    salary = models.DecimalField(_('Starting Salary'),help_text='This is the initial salary of employee',max_digits=16, decimal_places=2,null=True,blank=False)
    basic = models.CharField(blank=False,null=False, max_length=250)
    housing = models.CharField(blank=False,null=False, max_length=250)
    transport = models.CharField(blank=False,null=False, max_length=250)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')
        ordering = ['-name','-account']


    def __str__(self):
        return self.name






class Emergency(models.Model):

    EMERGENCY_RELATIONSHIP = (
    ('FATHER','Father'),
    ('MOTHER','Mother'),
    ('SIS','Sister'),
    ('BRO','Brother'),
    ('UNCLE','Uncle'),
    ('AUNTY','Aunty'),
    ('HUSBAND','Husband'),
    ('WIFE','Wife'),
    ('FIANCE','Fiance'),
    ('COUSIN','Cousin'),
    ('FIANCEE','Fiancee'),
    ('NIECE','Niece'),
    ('NEPHEW','Nephew'),
    ('SON','Son'),
    ('DAUGHTER','Daughter'),
    )


    # access table: employee.emergency_set.
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(_('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    tel = PhoneNumberField(default='+234240000000', null = False, blank=False, verbose_name='Phone Number (Example +234240000000)', help_text= 'Enter number with Country Code Eg. +234240000000')
    location = models.CharField(_('Place of Residence'),max_length= 125,null=True,blank=False)
    relationship = models.CharField(_('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default='Father',choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']


    def __str__(self):
        return self.fullname

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)








class Relationship(models.Model):
    STATUS = (
    ('Married','Married'),
    ('Single','Single'),
    ('Divorced','Divorced'),
    ('Widow','Widow'),
    ('Widower','Widower'),
    )

    NEXTOFKIN_RELATIONSHIP = (
    ('Father','Father'),
    ('Mother','Mother'),
    ('Sister','Sister'),
    ('Brother','Brother'),
    ('Uncle','Uncle'),
    ('Aunty','Aunty'),
    ('Husband','Husband'),
    ('Wife','Wife'),
    ('Fiance','Fiance'),
    ('Cousin','Cousin'),
    ('Fiancee','Fiancee'),
    ('Niece','Niece'),
    ('Nephew','Nephew'),
    ('Son','Son'),
    ('Daughter','Daughter'),
    )




    # access table: employee.relationship_set.or related_name = 'relation' employee.relation.***
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(_('Marital Status'),max_length=10,default='Single',choices=STATUS,blank=False,null=True)
    spouse = models.CharField(_('Spouse (Fullname)'),max_length=255,blank=True,null=True)
    occupation = models.CharField(_('Occupation'),max_length=125,help_text='spouse occupation',blank=True,null=True)
    tel = PhoneNumberField(default=None, null = True, blank=True, verbose_name='Spouse Phone Number (Example +234240000000)', help_text= 'Enter number with Country Code Eg. +234240000000')
    children = models.PositiveIntegerField(_('Number of Children'),null=True,blank=True,default=0)

    #recently added - 29/03/19
    nextofkin = models.CharField(_('Next of Kin'),max_length=255,blank=False,null=True,help_text='fullname of next of kin')
    contact = PhoneNumberField(verbose_name='Next of Kin Phone Number (Example +233240000000)',null=True,blank=True,help_text='Phone Number of Next of Kin')
    relationship = models.CharField(_('Relationship with Next of Person'),help_text='Who is this person to you ?',max_length=15,choices=NEXTOFKIN_RELATIONSHIP,blank=False,null=True)
    
    # close recent

    father = models.CharField(_('Father\'s Name'),max_length=255,blank=True,null=True)
    foccupation = models.CharField(_('Father\'s Occupation'),max_length=125,help_text='',blank=True,null=True)

    mother = models.CharField(_('Mother\'s Name'),max_length=255,blank=True,null=True)
    moccupation = models.CharField(_('Mother\'s Occupation'),max_length=125,help_text='',blank=True,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'
        ordering = ['created']

class Employee(models.Model):
    
    RELIGION = (
        ('Islam','Islam'),
        ('Christianity','Christianity'),
        ('Other','Other'),
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


    # PERSONAL DATA
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    title = models.CharField(_('Title'),max_length=5,default='Mr',choices=TITLE,blank=False,null=True)
    image = models.ImageField(_('Profile Image'),blank=True,null=True,help_text='upload image size less than 2.0MB', default='profile.png')#work on path username-date/image
    firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
    othername = models.CharField(_('Othername (optional)'),max_length=125,null=True,blank=True)
    sex = models.CharField(_('Gender'),max_length=9,default='Male',choices=GENDER,blank=False)
    email = models.CharField(_('Email (optional)'),max_length=255,default=None,blank=True,null=True)
    tel = PhoneNumberField(default='+234240000000', null = False, blank=False, verbose_name='Phone Number (Example +234240000000)', help_text= 'Enter number with Country Code Eg. +234240000000')
    bio = models.CharField(_('Bio'),help_text='Tell us something about yourself eg. i love eating ...',max_length=255,default='',null=True,blank=True)
    birthday = models.DateField(_('Birthday'),blank=False,null=False)
    religion = models.CharField(choices=RELIGION,verbose_name =_('Religion'),max_length=125,null=True,default=None)
    nationality = models.CharField(verbose_name =_('Nationality'),null=True,default=None, max_length=125)
    hometown = models.CharField(_('Hometown'),max_length=125,null=True,blank=True)
    residence = models.CharField(_('Current Residence'),max_length=125,null=False,blank=False)
    address = models.CharField(_('Address'),help_text='address of current residence',max_length=125,null=True,blank=True)
    
    education = models.CharField(_('Education'),help_text='highest educational standard ie. your last level of schooling',max_length=20,default='Senior_High',choices=EDUCATIONAL_LEVEL,blank=False,null=True)
    lastwork = models.CharField(_('Last Place of Work'),help_text='Employees Last place of Work',max_length=125,null=True,blank=True)
    position = models.CharField(_('Position Held'),help_text='Employees position at last place of work',max_length=255,null=True,blank=True)
    ssnitnumber = models.CharField(_('SSNIT Number'),max_length=30,null=True,blank=True)
    tinnumber = models.CharField(_('TIN'),max_length=15,null=True,blank=True)



    # COMPANY DATA
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    role        =   models.CharField(_('Position Held'), help_text='Position Held', blank=False, null=True, max_length=255)
    startdate = models.DateField(_('Employement Date'),help_text='Date of Employment',blank=False,null=True)
    employeetype = models.CharField(_('Employee Type'),max_length=15,default='Full_Time',choices=EMPLOYEETYPE,blank=False,null=True)
    employeeid = models.CharField(_('Employee ID Number'),max_length=11,help_text='Enter 5 characters, First and Last Letter of the department in caps followed by 3 numbers. e.g Finance (FE001)',null=True,blank=True)
    dateissued = models.DateField(_('Date Issued'),help_text='Date Employee id was issued',blank=False,null=True)

    #app related
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)
 
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    #PLUG MANAGERS
    objects = EmployeeManager()

    
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']



    def __str__(self):
        return self.get_full_name
        
    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername
        

        if (firstname and lastname) != None and othername is None:
            fullname = f'{lastname} {firstname}'
        elif othername != None:
            fullname = f'{lastname} {firstname} {othername}'
        return fullname


    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return



    @property
    def can_apply_leave(self):
        pass




    @property
    def get_pretty_birthday(self):
        if self.birthday:
            return self.birthday.strftime('%A,%d %B') # Thursday,04 May -> staffs age privacy
        return




    @property
    def birthday_today(self):
        '''
        returns True, if birthday is today else False
        '''
        return self.birthday.day == datetime.date.today().day



    @property
    def days_check_date_fade(self):
        '''
        Check if Birthday has already been celebrated ie in the Past     ie. 4th May  & today 8th May 4 < 8 -> past else present or future '''
        return self.birthday.day < datetime.date.today().day #Assumption made,If that day is less than today day,in the past




    def birthday_counter(self):
        '''
        This method counts days to birthday -> 2 day's or 1 day
        '''
        today = datetime.date.today()
        current_year = today.year

        birthday = self.birthday # eg. 5th May 1995

        future_date_of_birth = datetime.date(current_year,birthday.month,birthday.day)#assuming born THIS YEAR ie. 5th May 2019

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' days'

            else:

                return ' Tomorrow'

        return





    # def save(self,*args,**kwargs):
    #     '''
    #     overriding the save method - for every instance that calls the save method 
    #     perform this action on its employee_id

    #     '''
    #     get_id = self.employeeid #grab employee_id number from submitted form field
    #     data = code_format(get_id)
    #     self.employeeid = data #pass the new code to the employee_id as its orifinal or actual code
    #     super().save(*args,**kwargs) # call the parent save method
    #     # print(self.employeeid)

class Payroll(models.Model):
    Month = (
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December'),
    )
    
    Year = (
    ('2020','2020'),
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),
    ('2026','2026'),
    ('2027','2027'),
    ('2028','2028'),
    ('2029','2029'),
    ('2030','2030'),
    ('2031','2031'),
    )
    employ = models.ForeignKey('Employee',on_delete=models.CASCADE,default=None, blank=True,)
    bank = models.ForeignKey('Bank',on_delete=models.CASCADE,null=True,blank=True)
    paymentdate = models.DateField(blank=True,null=False, max_length=250)
    overtime = models.CharField(blank=True,null=False, max_length=250, default=0)
    basic_m = models.CharField(blank=False,null=False, max_length=250)
    housing_m = models.CharField(blank=False,null=False, max_length=250)
    transport_m = models.CharField(blank=False,null=False, max_length=250)
    pension = models.CharField(blank=True,null=False, max_length=250)
    paye = models.CharField(blank=False,null=False, max_length=250)
    loan = models.CharField(blank=True,null=True, max_length=250, default=0)
    bonus = models.CharField(blank=True,null=True, max_length=250, default=0)
    gross = models.CharField(blank=True,null=True, max_length=250, default=0)
    totald = models.CharField(blank=True,null=True, max_length=250, default=0)
    netpay = models.CharField(blank=True,null=True, max_length=250, default=0)
    deductther = models.CharField(blank=True,null=True, max_length=250, default=0)
    month = models.CharField(choices=Month, max_length=250, blank=True,null=True)
    Year = models.CharField(choices=Year, max_length=250, blank=True,null=True)