from django.contrib.auth.models import User
from django import forms
from .models import Campaign, Donation

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['user', 'amount_raised']
        fields =  '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


    # def clean(self):
    #     """
    #     Perform custom validation that involves multiple fields.
    #     This is called after the individual field clean methods.
    #     """
    #     cleaned_data = super().clean()  # Get the cleaned data for all fields

    #     # Access fields directly from the cleaned data dictionary
    #     title = cleaned_data.get('title')
    #     description = cleaned_data.get('description')
    #     goal_amount = cleaned_data.get('goal_amount')

    #     # Example Validation:
    #     # 1. Ensure that the title is not empty
    #     if not title or len(title.strip()) == 0:
    #         raise forms.ValidationError({'title': 'Title cannot be empty.'})

    #     # 2. Ensure that the goal amount is greater than zero
    #     if goal_amount is not None and goal_amount <= 0:
    #         raise forms.ValidationError({'goal_amount': 'Goal amount must be greater than zero.'})

    #     # 3. Ensure that the description is long enough if the goal amount is very high
    #     if goal_amount and goal_amount > 10000 and (not description or len(description.strip()) < 50):
    #         raise forms.ValidationError({'description': 'Description must be at least 50 characters long for high goal amounts.'})

    #     return cleaned_data




class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['campaign', 'user', 'payment_status']
        fields = '__all__'


class PaymentForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    expiry_month = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'placeholder': 'Expiry Month (MM)'}))
    expiry_year = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'placeholder': 'Expiry Year (YY)'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    security_code = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'Security Code (CVV)'}))