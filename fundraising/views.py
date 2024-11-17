from django.shortcuts import render, redirect,get_object_or_404
from .forms import CampaignForm, DonationForm, PaymentForm, WithdrawalForm
from .models import Campaign, Donation, Withdrawal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .payment_api import charge_card, transfer_funds
import uuid, json
from django.db import transaction

# logger = logging.getLogger(__name__)
# logger = logging.getLogger('django.db.backends')
# logger.setLevel(logging.DEBUG)



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
            return redirect('donationpage')
        else:
            messages.error(request, 'incorrect information')
    else:
        form = CampaignForm()
    return render(request, 'campaign.html', {'form' : form})

@login_required(login_url='login')
def campaign_info(request):
    try:
        campaign = Campaign.objects.get(user=request.user)
        return render(request, 'campaignpage.html', {'campaign': campaign})
    except Campaign.DoesNotExist:
        return render(request, 'nocampaign.html')


def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def default_donation_page(request):
    campaigns = Campaign.objects.all()
    return render(request, 'donationpage.html', {'campaigns': campaigns })


@login_required(login_url='login')
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
            messages.error(request, 'please fill out the form')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form, 'campaign': campaign})

@login_required(login_url='login')
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
            

            try:
                charge_success = charge_card(first_name, last_name, email_address, phone_number,
                                            card_number, expiry_month, expiry_year, security_code, pay_amount)
                
                # Decoding the JSON content into a Python dictionary
                try:
                    charge_success_data = json.loads(charge_success.content)  # Parse the JSON content
                    # Now access the 'statusOk' key
                    if charge_success_data('do3dsAuth'):
                        creq = charge_success_data('formData')  # This would generate the cryptogram (creq) for 3D Secure
                        threeDsUrl = "https://mtf.gateway.mastercard.com/acs/visa/v2/prompt"  
                        response_data = {
                            'statusOk': {charge_success_data['statusOk']},
                            'do3dsAuth': True,
                            'threeDsUrl': threeDsUrl,
                            'formData': creq  # Cryptogram for 3D Secure
                        }
                        return JsonResponse(response_data)
                    elif charge_success_data["do3dsAuth"] == False & charge_success_data['statusOk'] : 
                        donation_id = uuid.uuid4()
                        with transaction.atomic():
                            # Create the donation record
                            donation = Donation(
                                user_id=request.user.id,
                                amount=pay_amount,
                                campaign=campaign,
                                donation_id=donation_id,
                                payment_status='success',  # Payment successful
                            )

                            donation.save() 
                            messages.success(request, "Donation Successful, Yay it's a great day")
                            # On success, redirect the user to a success page or show a success message
                            return redirect('payment_success')                      
                    else:
                        # Payment failed, show error message from charge_success

                        return render(request, 'auths/payment_failure.html', {'messages': charge_success_data['message']})
                except Exception as e:
                    # Optionally, show an error page or log the issue for further debugging
                    messages.error(request, 'please enter correct information')
                    return render(request, 'auths/payment_failure.html', {'error': str(e)})
            except Exception as e:
                # Handle payment failure
                return render(request, 'auths/payment_failure.html', {'error': str(e)})
        else:
            messages.error(request, 'incorrect credentials')              
    else:
        form = PaymentForm(initial={'amount': amount})  # Set initial value here
    return render(request, 'auths/payment_form.html', {'form': form, 'campaign': campaign, 'amount': amount})


@login_required(login_url='login')
def payment_success(request):
    return render(request, 'auths/payment_success.html')



def about_view(request):
    return render(request, 'about.html')

def team(request):
    return render(request, 'team.html')

def causes(request):
    return render(request, 'causes.html')

def event(request):
    return render(request, 'event.html')


@login_required
def withdraw_view(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            
            amount = form.cleaned_data['amount']
            account_number = form.cleaned_data['account_number']
            account_name = form.cleaned_data['account_name']
            bank_code = form.cleaned_data['bank_code']
            narration = form.cleaned_data.get('narration', '')
            transaction_ref_num = uuid.uuid4()
           
            
            withdrawal = Withdrawal(
                user=request.user,
                amount=amount,
                account_number=account_number,
                account_name=account_name,
                transaction_ref_num= transaction_ref_num,  
            )

            transfer_response = transfer_funds(amount, account_name, account_number, bank_code, narration, transaction_ref_num)
            print(transfer_response)

            transfer_response_data = json.loads(transfer_response.content)  

            if transfer_response_data.get('statusOk'): 

                withdrawal.save()
                messages.success(request, 'Withdrawal request submitted successfully!')
                return redirect('withdraw_success')  # Redirect to a success page
            else:
                messages.error(request, f"Error: {transfer_response.get('message', 'Withdrawal failed.')}")
                return redirect('withdraw')  # Optionally redirect back to the withdrawal form

    else:
        form = WithdrawalForm()

    return render(request, 'auths/withdraw.html', {'form': form})

@login_required(login_url='login')
def payment_failed(request):
    return render(request, 'auths/payment_failure.html')