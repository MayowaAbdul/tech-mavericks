from django.contrib import admin
from .models import Campaign
from django.contrib.auth.models import User

# Register your models here
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign_purpose', 'created_at','goals', 'amount_raised' ]




