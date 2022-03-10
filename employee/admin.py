from django.contrib import admin
from employee.models import Department,Employee,Bank,Emergency,Relationship, Payroll


class PayrollAdmin(admin.ModelAdmin):
    list_display	=	['employ','month','Year',]   
    
class RelationshipAdmin(admin.ModelAdmin):
    list_display	=	['employee','status',] 
    
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Bank)
admin.site.register(Emergency)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Payroll, PayrollAdmin)