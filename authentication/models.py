from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    country_choices = [
        ('Nigeria', 'nigeria'),
        ('South Africa', 'south africa')
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, choices=country_choices, blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)




    
