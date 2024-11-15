from django.contrib import admin
from .models import Campaign, Donation
from django.contrib.auth.models import User

# Register your models here
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign_purpose', 'created_at','goals', 'amount_raised' ]

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['user','payment_status', 'amount', 'donated_at', 'message']




