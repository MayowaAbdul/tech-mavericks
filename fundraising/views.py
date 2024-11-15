from django.shortcuts import render, redirect,get_object_or_404
from .forms import CampaignForm, DonationForm, PaymentForm
from .models import Campaign, Donation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .payment_api import charge_card
import uuid
from django.db import transaction


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
        form = DonationForm(request.POST)
        if form.is_valid():
            donate = form.save(commit=False)
            donate.user = request.user
            donate.campaign_id = campaign_id
            amount = donate.amount

            return redirect('process_payment', amount=amount, campaign_id=campaign_id)
        else:
            messages.error(request, 'please correct the errors')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form, 'campaign': campaign})


def process_payment(request, amount, campaign_id ):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            #making api payment
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_address = form.cleaned_data['email_address']
            phone_number = form.cleaned_data['phone_number']
            card_number = form.cleaned_data['card_number']
            expiry_month = form.cleaned_data['expiry_month']
            expiry_year = form.cleaned_data['expiry_year']
            security_code = form.cleaned_data['security_code']
            pay_amount = float(amount)
            print(pay_amount)
            print(form.cleaned_data)


            try:
                charge_success = charge_card(first_name, last_name, email_address, phone_number,
                                             card_number, expiry_month, expiry_year, security_code, pay_amount)
                
                if charge_success["success"]: 
                    donation_id = uuid.uuid4()  # Generate a unique donation ID

                    with transaction.atomic():
                        # Create the donation record
                        donation = Donation(
                            user_id=request.user,
                            amount=pay_amount,
                            campaign=campaign,
                            donation_id=donation_id,
                            payment_status='success',  # Payment successful
                        )
                        donation.save() 

                        campaign.amount_raised += pay_amount
                        campaign.save()
                        # On success, redirect the user to a success page or show a success message
                    return redirect('payment_success')  
                else:
                    # Payment failed, show error message from charge_success
                    return render(request, 'auths/payment_failure.html', {'error': charge_success['message']})

            except Exception as e:
                # Handle payment failure
                return render(request, 'auths/payment_failure.html', {'error': str(e)})
            
    else:
        form = PaymentForm(initial={'amount': amount})  # Set initial value here
    return render(request, 'auths/payment_form.html', {'form': form, 'campaign': campaign, 'amount': amount})


def payment_success(request):
    return render(request, 'auths/payment_success.html')

def about_view(request):
    return render(request, 'about.html')