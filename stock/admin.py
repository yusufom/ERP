from django.contrib import admin
from .models import Stock, Category, StockLog, Location
from .forms import StockCreateForm, StockLogSearchForm

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
    
class StockLogAdmin(admin.ModelAdmin):
    list_display = ['category', 'action', 'action_by', 'datefield']
    model = StockLogSearchForm
    list_filter = ['category']
    search_fields = ['category', 'action_by', 'start_date', 'end_date']
    
    
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(StockLog, StockLogAdmin)