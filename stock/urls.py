from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('dashboard/Inventory/list_item/', views.list_item, name='list_item'),
    path('dashboard/Inventory/cat_list/', views.cat_list, name='cat_list'),
    path('dashboard/Inventory/loc_list/', views.loc_list, name='loc_list'),
    path('dashboard/Inventory/add_items/', views.add_items, name='add_items'),
    path('dashboard/Inventory/update_items/<str:pk>/', views.update_items, name="update_items"),
    path('dashboard/Inventory/delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('dashboard/Inventory/stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('dashboard/Inventory/stocklist_cat/<str:pk>/', views.stocklist_cat, name="stocklist_cat"),
    path('dashboard/Inventory/stocklist_loc/<str:pk>/', views.stocklist_loc, name="stocklist_loc"),
    path('dashboard/Inventory/issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('dashboard/Inventory/receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('dashboard/Inventory/reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('dashboard/Inventory/list_history/', views.list_history, name='list_history'),
    path('dashboard/Inventory/add_category/', views.add_category, name='add_category'),
    path('dashboard/Inventory/add_location/', views.add_location, name='add_location'),
    
]