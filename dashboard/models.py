from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

User=settings.AUTH_USER_MODEL

# Create your models here.
class dashboard(models.Model):
    number = models.CharField(max_length=5,null=True,blank=True)
    mssg = models.CharField(max_length=10000,null=False,blank=False)
    img = models.ImageField(blank=True,null=True)

class todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=5000, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    duedate = models.DateField(max_length=100, blank=True,null=True)
    
    def __str__(self):
        return self.title