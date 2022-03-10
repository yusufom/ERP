from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

User=settings.AUTH_USER_MODEL

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    condition = (
		('Good', 'Good'),
		('Okay', 'Okay'),
		('Bad', 'Bad'),
	)
    unit = (
		('Length', 'Length'),
		('Pieces', 'Pieces'),
		('Roll', 'Roll'),
        ('Bucket', 'Bucket'),
	)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name='stocks')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, related_name='stocks')
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True, choices=unit)
    condition = models.CharField(max_length=50, blank=True, null=True, choices=condition)
    comment =   models.TextField(max_length=2000, blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_from = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    datefield = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.item_name
    
class StockLog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=255)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    datefield = models.DateTimeField()