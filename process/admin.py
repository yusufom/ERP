from django.contrib import admin
from django import forms
from django.forms import fields
from .models import Compound, Element, ElementAll, VaporPressureOfIOL,   DensityOfIOL, CriticalConstantsAndAFIOC, HeatofVaporizationOIOL, HeatCapacityOIOL, HeatCapacityAtConstantPOIOLpolynomial, HeatCapacityAtConstantPOIOLhyperbolic, EnthalpyandGibbs, VaporViscosityIOS, ViscosityofIOL, VaporThermalofIOS, ThermalConductivityofIOL
from ckeditor.widgets import CKEditorWidget 
from import_export.admin import ImportExportModelAdmin

class VaporPressureOfIOLAdmin(admin.TabularInline):
    model = VaporPressureOfIOL
    extra = 1


class DensityOfIOLAdmin(admin.TabularInline):
    model = DensityOfIOL
    extra = 1    

class CriticalConstantsAndAFIOCAdmin(admin.TabularInline):
    model = CriticalConstantsAndAFIOC
    extra = 1 

class HeatofVaporizationOIOLAdmin(admin.TabularInline):
    model = HeatofVaporizationOIOL
    extra = 1 
    
class HeatCapacityOIOLAdmin(admin.TabularInline):
    model = HeatCapacityOIOL
    extra = 1

class HeatCapacityAtConstantPOIOLpolynomialAdmin(admin.TabularInline):
    model = HeatCapacityAtConstantPOIOLpolynomial
    extra = 1
    
class HeatCapacityAtConstantPOIOLhyperbolicAdmin(admin.TabularInline):
    model = HeatCapacityAtConstantPOIOLhyperbolic
    extra = 1
    
class EnthalpyandGibbsAdmin(admin.TabularInline):
    model = EnthalpyandGibbs
    extra = 1

class VaporViscosityIOSAdmin(admin.TabularInline):
    model = VaporViscosityIOS
    extra = 1
    
class ViscosityofIOLAdmin(admin.TabularInline):
    model = ViscosityofIOL
    extra = 1
    
class VaporThermalofIOSAdmin(admin.TabularInline):
    model = VaporThermalofIOS
    extra = 1
    
class ThermalConductivityofIOLAdmin(admin.TabularInline):
    model = ThermalConductivityofIOL
    extra = 1

# class ElementAllAdmin(admin.ModelAdmin):
#     inlines = [VaporPressureOfIOLAdmin, DensityOfIOLAdmin, CriticalConstantsAndAFIOCAdmin, HeatofVaporizationOIOLAdmin, HeatCapacityOIOLAdmin, HeatCapacityAtConstantPOIOLpolynomialAdmin, HeatCapacityAtConstantPOIOLhyperbolicAdmin, EnthalpyandGibbsAdmin, VaporViscosityIOSAdmin, ViscosityofIOLAdmin, VaporThermalofIOSAdmin, ThermalConductivityofIOLAdmin,]
#     list_display = ['name', 'formula', 'CASno', 'molwt']

class ElementAllAdmin(ImportExportModelAdmin):
    inlines = [VaporPressureOfIOLAdmin, DensityOfIOLAdmin, CriticalConstantsAndAFIOCAdmin, HeatofVaporizationOIOLAdmin, HeatCapacityOIOLAdmin, HeatCapacityAtConstantPOIOLpolynomialAdmin, HeatCapacityAtConstantPOIOLhyperbolicAdmin, EnthalpyandGibbsAdmin, VaporViscosityIOSAdmin, ViscosityofIOLAdmin, VaporThermalofIOSAdmin, ThermalConductivityofIOLAdmin,]
    list_display = ['name', 'formula', 'CASno', 'molwt']
    
admin.site.register(Compound)
admin.site.register(ElementAll, ElementAllAdmin)
admin.site.register(Element)