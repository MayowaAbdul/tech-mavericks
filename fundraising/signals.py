from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation

@receiver(post_save, sender=Donation)
def update_raised_amount(sender, instance, created, **kwargs):
    if created:
        campaign = instance.campaign
       
        campaign.amount_raised += int(instance.amount)
        campaign.save()
    else:
        print('campaign coulf not be created')