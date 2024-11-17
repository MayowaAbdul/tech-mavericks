from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Donation)
def update_raised_amount(sender, instance, created, **kwargs):
    if created:
        logger.info(f'Donation created: {instance.amount} for campaign {instance.campaign.title}')
        campaign = instance.campaign
        logger.info(f'Previous amount_raised: {campaign.amount_raised}')
        campaign.amount_raised += int(instance.amount)
        campaign.save()
        logger.info(f'Updated amount_raised: {campaign.amount_raised}')
    else:
        print('campaign coulf not be created')