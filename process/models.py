from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

User=settings.AUTH_USER_MODEL


class Compound(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Element(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    img = models.ImageField(blank=True,null=True,help_text='upload image size less than 2.0MB', default='profile.png')
    
    def __str__(self):
        return self.name
    
class ElementAll(models.Model):
    compound = models.ForeignKey('Compound', on_delete=models.CASCADE, blank=True)
    element = models.ForeignKey('Element', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    formula= RichTextUploadingField(max_length=200,blank=True, null=True)
    CASno = models.CharField(max_length=300,blank=True, null=True)
    molwt = models.CharField(max_length=300,blank=True, null=True)
    formular_weight= models.CharField(max_length=300,blank=True, null=True)
    color= models.CharField(max_length=300,blank=True, null=True)
    crystalline_form= models.CharField(max_length=300,blank=True, null=True)
    refractive_index= models.CharField(max_length=300,blank=True, null=True)
    specific_gravity= RichTextUploadingField(max_length=300,blank=True, null=True)
    melting_point= RichTextUploadingField(max_length=300,blank=True, null=True)
    boiling_point= RichTextUploadingField(max_length=300,blank=True, null=True)
    solubility_cold = RichTextUploadingField(max_length=300,blank=True, null=True)
    solubility_hot= RichTextUploadingField(max_length=300,blank=True, null=True)
    solubility_other= RichTextUploadingField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"

class  VaporPressureOfIOL(models.Model):
    el = models.ForeignKey(ElementAll, related_name='VaporpressureOfIOL', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    C5= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    PTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    PTmax= models.CharField(max_length=2000, blank=True, null=True)
        
class  DensityOfIOL(models.Model):
    el = models.ForeignKey(ElementAll, related_name='DensityOfIOl', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    DTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    DTmax= models.CharField(max_length=2000, blank=True, null=True)
    
class  CriticalConstantsAndAFIOC(models.Model):
    el = models.ForeignKey(ElementAll, related_name='CriticalconstantsAndAFIOC', blank=True, on_delete=models.CASCADE)
    Tc= models.CharField(max_length=2000, blank=True, null=True)
    Pc= models.CharField(max_length=2000, blank=True, null=True)
    Vc= models.CharField(max_length=2000, blank=True, null=True)
    Zc= models.CharField(max_length=2000, blank=True, null=True)
    AccentricFactor= models.CharField(max_length=2000, blank=True, null=True)
    
class  HeatofVaporizationOIOL(models.Model):
    el = models.ForeignKey(ElementAll, related_name='HeatofvaporizationOIOL', blank=True, on_delete=models.CASCADE)
    C1x07= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    HvTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    HvTmax= models.CharField(max_length=2000, blank=True, null=True)
    
class  HeatCapacityOIOL(models.Model):
    Equation = (
    ('1','1'),
    ('2','2'),
    )
    el = models.ForeignKey(ElementAll, related_name='HeatcapacityOIOL', blank=True, on_delete=models.CASCADE)
    eqn = models.CharField(max_length=2000, blank=True, null=True, choices=Equation)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    C5= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    CpTminE05= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    CpTmaxE05= models.CharField(max_length=2000, blank=True, null=True)
    
class  HeatCapacityAtConstantPOIOLpolynomial(models.Model):
    el = models.ForeignKey(ElementAll, related_name='HeatcapacityAtConstantPOIOLpolynomial', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4E05= models.CharField(max_length=2000, blank=True, null=True)
    C5E10= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    CpTminE05= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    CpTmaxE05= models.CharField(max_length=2000, blank=True, null=True)
    
class  HeatCapacityAtConstantPOIOLhyperbolic(models.Model):
    el = models.ForeignKey(ElementAll, related_name='HeatcapacityAtConstantPOIOLhyperbolic', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3E03= models.CharField(max_length=2000, blank=True, null=True)
    C4E05= models.CharField(max_length=2000, blank=True, null=True)
    C5= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    CpTminE05= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    CpTmaxE05= models.CharField(max_length=2000, blank=True, null=True)
    
class  EnthalpyandGibbs(models.Model):
    el = models.ForeignKey(ElementAll, related_name='Enthalpyandgibbs', blank=True, on_delete=models.CASCADE)
    IdealgasEnthalpyE07= models.CharField(max_length=2000, blank=True, null=True)
    IdealgasGibbsE07= models.CharField(max_length=2000, blank=True, null=True)
    IdealgasEntropyE05= models.CharField(max_length=2000, blank=True, null=True)
    StandardnetEnthalpyE09= models.CharField(max_length=2000, blank=True, null=True)
    
class  VaporViscosityIOS(models.Model):
    el = models.ForeignKey(ElementAll, related_name='VaporviscosityIOS', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    VsTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    VsTmax= models.CharField(max_length=2000, blank=True, null=True)

class  ViscosityofIOL(models.Model):
    el = models.ForeignKey(ElementAll, related_name='ViscosityofIOl', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    C5= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    VsTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    VsTmax= models.CharField(max_length=2000, blank=True, null=True)
    
class  VaporThermalofIOS(models.Model):
    el = models.ForeignKey(ElementAll, related_name='VaporthermalofIOS', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    TCTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    TCTmax= models.CharField(max_length=2000, blank=True, null=True)
    
class  ThermalConductivityofIOL(models.Model):
    el = models.ForeignKey(ElementAll, related_name='ThermalconductivityofIOL', blank=True, on_delete=models.CASCADE)
    C1= models.CharField(max_length=2000, blank=True, null=True)
    C2= models.CharField(max_length=2000, blank=True, null=True)
    C3= models.CharField(max_length=2000, blank=True, null=True)
    C4= models.CharField(max_length=2000, blank=True, null=True)
    C5= models.CharField(max_length=2000, blank=True, null=True)
    Tmin= models.CharField(max_length=2000, blank=True, null=True)
    TCTmin= models.CharField(max_length=2000, blank=True, null=True)
    Tmax= models.CharField(max_length=2000, blank=True, null=True)
    TCTmax= models.CharField(max_length=2000, blank=True, null=True)