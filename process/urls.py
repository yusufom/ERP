from django.urls import path
from . import views

app_name = 'process'

urlpatterns = [
    path('dashboard/process/', views.pro_home, name='ProceesHome'),
    path('dashboard/process/view/<int:id>/', views.element_detail, name='ProceesDet'),
    # path('dashboard/process/search_auto/', views.search_auto, name='search_auto'),
]