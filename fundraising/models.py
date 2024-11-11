from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()
# Create your models here.


class Campaign(models.Model):
    campaign_choices = [
        ('Child Education', 'child education'),
        ('Child Healthare', 'child healthcare')
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture', null=True)
    title = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=50, null=True, default='+1-6574-323-233')
    goals = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    amount_raised = models.DecimalField(null=True, default=0,decimal_places=2, max_digits=10 )
    campaign_purpose = models.CharField(max_length=50, choices=campaign_choices, null=True, default='Child Education')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def current_amount(self):
        return (donation.amount for donation in self.donation.all())
    

class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    donated_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    message = models.CharField(max_length=100, null=True, default='')

    def __str__(self):
        return f"{self.user.username} donated to {self.campaign.title}"