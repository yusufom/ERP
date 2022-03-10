from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_login, name='Login'),
    path('logout/',views.logout_view,name='Logout'),
    path('dashboard/profile/',views.user_profile_view, name='Userprofile'),
    path('dashboard/profile/change-password/',views.changepassword,name='Changepassword'),
    path('dashboard/employees/create-user/', views.register_user_view,name='Register'),
    
]