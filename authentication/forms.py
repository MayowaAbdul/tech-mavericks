from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile


class AccountCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    agreed_to_terms = forms.BooleanField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'agreed_to_terms']

class ProfileForm(forms.ModelForm):
    country = forms.ChoiceField()
    class Meta:
        model = Profile
        fields = ['profile_picture', 'street', 'city', 'state', 'country', 'phone_number']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'country': forms.RadioSelect()
        }


