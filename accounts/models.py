from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_HR = models.BooleanField(default=False)
    is_FM = models.BooleanField(default=False)
    is_Manager = models.BooleanField(default=False)
    is_Employee = models.BooleanField(default=False)
    signature = models.ImageField(default=None,blank=True, null=True)
    
    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name}'