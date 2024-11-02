from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AccountCreationForm, ProfileForm
from .models import Profile

# Create your views here.


def register(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'signup successful, please login')

            #redirecting to the login page 
            return redirect('login')
        else:
            messages.error(request, 'incorrect credentials')
    else:
        form = AccountCreationForm()
    return render(request, 'auths/registration.html', {"forms" : form })


def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user=user)
                    return redirect('home')
                else:
                    messages.error(request, 'User with this email or password does not exist')
            else:
                messages.error(request, 'please kindly check your info')    
        return render(request, 'auths/login.html')
    

def logout_view(request):
    logout(request)
    messages.success(request, 'you logged out successfully')
    return redirect('login')

def profile(request):
    form = ProfileForm()
    return render(request, 'auths/settings.html', {'forms': form})
