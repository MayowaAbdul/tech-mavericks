from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class AccountCreation(AbstractUser):

    Agreed_to_terms = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    #user permissions 

    groups = models.ManyToManyField(Group, related_name='AccountCreations')
    user_permissions = models.ManyToManyField(Permission, related_name='AccountCreation_permissions')
    


class Profile(models.Model):
    country_choices = [
        ('Nigeria', 'nigeria'),
        ('South Africa', 'south africa')
    ]


    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture', null=True)
    street = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=30, choices=country_choices, null=True, default='Nigeria')
    phone_number = models.CharField(max_length=50, null=True, default='+1-6574-323-233')

    def __str__(self):
        return self.country




    
