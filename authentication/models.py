from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    country_choices = [
        ('Nigeria', 'nigeria'),
        ('South Africa', 'south africa')
    ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, choices=country_choices, blank=True)

    def __str__(self):
        return self.user.username






    
