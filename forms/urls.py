from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'forms'

urlpatterns = [
    # path('', views.PurchaseOrderListView.as_view(), name="po-list"),
    # path('view/<id>/', views.invoiceview, name="viewinvoice"),
    path('dashboard/po/create-po/', views.createPO, name="createPO"),
    path('dashboard/po/view-po/', views.view_PO, name="viewPO"),
    path('dashboard/po/view-po/<id>/', views.view_one, name="viewPONE"),
    path('dashboard/po/view-po/pdf_view/<id>/', views.render_pdf_view, name="pdfview"),
    path('dashboard/po/view-po/pdf_download/<id>/', views.download_pdf_view, name="pdfdownload"),
    path('dashboard/po/view-po/approve/<int:id>/',views.approve_PO,name='POapprove'),
    path('dashboard/po/view-po/unapprove/<int:id>/',views.unapprove_PO,name='unPOapprove'),
    path('dashboard/po/view-po/reject/<int:id>/',views.reject_PO,name='POreject'),
    path('dashboard/po/view-po/unreject/<int:id>/',views.unreject_PO,name='unPOreject'),
    
    #Request Form
    path('dashboard/rf/create-rf/', views.createRF, name="createRF"),
    path('dashboard/rf/view-rf/', views.view_RF.as_view(), name="viewRF"),
    path('dashboard/rf/view-rf/<id>/', views.view_onerf, name="viewRFONE"),
    path('dashboard/rf/view-rf/pdf_view/<id>/', views.rfrender_pdf_view, name="rfpdfview"),
    path('dashboard/rf/view-rf/pdf_download/<id>/', views.rfdownload_pdf_view, name="rfpdfdownload"),
    
    path('dashboard/po/view-rf/approve/<int:id>/',views.approve_RF,name='RFapprove'),
    path('dashboard/po/view-rf/unapprove/<int:id>/',views.unapprove_RF,name='unRFapprove'),
    path('dashboard/po/view-rf/reject/<int:id>/',views.reject_RF,name='RFreject'),
    path('dashboard/po/view-rf/unreject/<int:id>/',views.unreject_RF,name='unRFreject'),
    
    path('dashboard/po/view-rf/fapprove/<int:id>/',views.fapprove_RF,name='fRFapprove'),
    path('dashboard/po/view-rf/funapprove/<int:id>/',views.funapprove_RF,name='unfRFapprove'),
    path('dashboard/po/view-rf/freject/<int:id>/',views.freject_RF,name='fRFreject'),
    path('dashboard/po/view-rf/funreject/<int:id>/',views.funreject_RF,name='unfRFreject'),
]