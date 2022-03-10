from django.db import models
import datetime

class POManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()



	def all_pending_po(self):
		return super().get_queryset().filter(status = 'Pending').order_by('-created')# applying FIFO 




	def all_cancel_po(self):
		return super().get_queryset().filter(status = 'Cancelled').order_by('-created')




	def all_rejected_po(self):
		return super().get_queryset().filter(status = 'Rejected').order_by('-created')




	def all_approved_po(self):
		return super().get_queryset().filter(status = 'Approved')



	def current_year_leaves(self):
		return super().get_queryset().filter(startdate__year = datetime.date.today().year)


class RFManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def all_pending_po(self):
        return super().get_queryset().filter(status = 'Pending').order_by('-created')# applying FIFO 
    
    def all_cancel_po(self):
        return super().get_queryset().filter(status = 'Cancelled').order_by('-created')
    
    def all_rejected_po(self):
        return super().get_queryset().filter(status = 'Rejected').order_by('-created')
    
    def all_approved_po(self):
        return super().get_queryset().filter(status = 'Approved')
