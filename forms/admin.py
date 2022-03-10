from django.contrib import admin
from .models import Purchaseorder, Ordersummary, RequestForm, RFsummary
# Register your models here.

class OrdersummaryAdmin(admin.TabularInline):
    model = Ordersummary
    extra = 0

class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [OrdersummaryAdmin,]
    list_display	=	['order_no','user','approval','created',]
    
class RFsummaryAdmin(admin.TabularInline):
    model = RFsummary
    extra = 0

class RequestFormAdmin(admin.ModelAdmin):
    inlines = [RFsummaryAdmin,]
    list_display	=	['cctr','user','Manager_approval','created',]

admin.site.register(Ordersummary)
admin.site.register(Purchaseorder, PurchaseOrderAdmin)
admin.site.register(RFsummary)
admin.site.register(RequestForm, RequestFormAdmin)