from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.dashboardy, name='Dash'),
    path('dashboard/employees/',views.dashboard_employees,name='Employees'),
    path('dashboard/employees/create-user/add-employee',views.dashboard_employees_create,name='Employeecreate'),
    path('dashboard/employee/profile/edit/<int:id>/',views.employee_edit_data,name='Edit'),
    path('employee/profile/<int:id>/',views.dashboard_employee_info,name='Employeeinfo'),
    
    path('employee/emergency/',views.dashboard_emergency_add, name='EmergencyCreate'),
    
    path('emergency/update/<int:id>',views.dashboard_emergency_update,name='EmergencyUpdate'),

    # # Family
    path('family/create/',views.dashboard_family_create,name='FamilyAdd'),
    path('family/edit/<int:id>',views.dashboard_family_edit,name='FamilyUpdate'),
    
    #dept
    path('department/create/',views.depcreate,name='DeptAdd'),
    
    # #Bank
    path('bank/create/',views.dashboard_bank_create,name='BankinfoAdd'),
    path('bank/edit/<int:id>/',views.employee_bank_account_update,name='BankinfoEdit'),
    
    path('leave/apply/',views.leave_creation,name='CreateLeave'),
    path('leaves/pending/all/',views.pending_leaves_list,name='LeavesList'),
    path('leaves/approved/all/',views.leaves_approved_list,name='ApprovedleavesList'),
    path('leaves/cancel/all/',views.cancel_leaves_list,name='CanceleavesList'),
    path('leaves/all/view/<int:id>/',views.leaves_view,name='UserleaveView'),
    path('leave/approve/<int:id>/',views.approve_leave,name='userleaveapprove'),
    path('leave/unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    path('leave/cancel/<int:id>/',views.cancel_leave,name='userleavecancel'),
    path('leave/uncancel/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',views.leave_rejected_list,name='LeavesRejected'),
    path('leave/reject/<int:id>/',views.reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',views.unreject_leave,name='unreject'),
    # # BIRTHDAY ROUTE
    path('birthdays/all',views.birthday_this_month,name='birthdays'),
    
    path('payroll/',views.payrollcreate,name='Payroll'),
    path('payroll/all/',views.payrollall,name='PayrollAll'),
    path('payroll/user/all/',views.mypayrollall,name='MyPayrollAll'),
    path('payroll/view/<id>/', views.view_onepayroll, name="viewPayrollONE"),
    path('payroll/view/pdf_view/<id>/', views.render_pdf_viewpayroll, name="PdfviewPayroll"),
    path('payroll/view/pdf_download/<id>/', views.download_pdf_viewpayroll, name="PdfdownloadPayroll"),
    path('payroll/edit/<int:id>',views.edit_payroll,name='PayrollEdit'),
    path('payroll/duplicate/<int:id>',views.duplicate_payroll,name='PayrollDup'),
    
    #Todo
    path('todo/list/', views.TaskList.as_view(), name='TodoList'),
    path('todo/list/<int:pk>/', views.TaskDetail.as_view(), name='Tododet'),
    path('todo/task-create/', views.TaskCreate.as_view(), name='Todo-create'),
    path('todo/task-update/<int:pk>/', views.TaskUpdate.as_view(), name='Todo-update'),
    path('todo/task-delete/<int:pk>/', views.DeleteView.as_view(), name='Todo-delete'),
]