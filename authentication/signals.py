from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth.models import User

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)