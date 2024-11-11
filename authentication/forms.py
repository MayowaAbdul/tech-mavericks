from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User




class AccountCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    agree_to_terms = forms.BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'agree_to_terms']




