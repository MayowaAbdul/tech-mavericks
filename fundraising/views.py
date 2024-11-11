from django.shortcuts import render, redirect,get_object_or_404
from .forms import CampaignForm, DonationForm
from .models import Campaign
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def campaign_view(request):
    campaign = Campaign.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('donation_page')
        else:
            messages.error(request, 'incorrect information')
    else:
        form = CampaignForm()
    return render(request, 'campaign.html', {'form' : form})


def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def default_donation_page(request):
    campaigns = Campaign.objects.all()
    return render(request, 'donationpage.html', {'campaigns': campaigns })

def donation(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            donate = form.save(commit=False)
            donate.user = request.user
            donate.campaign_id = campaign_id
            donate.save()
            return redirect('campaign_details')
        else:
            messages.error(request, 'please correct the errors')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form, 'campaign': campaign})