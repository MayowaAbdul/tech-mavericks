from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AccountCreationForm, ProfileForm, AccountUpdateForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required



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
            return render(request,'auths/register.html', {"forms" : form } )
    else:
        form = AccountCreationForm()
    return render(request, 'auths/register.html', {"forms" : form })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.errors:
            print(form.errors)
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

@login_required(login_url='login')
def profile(request):
    address = get_object_or_404(Profile, user=request.user)
    return render(request, 'auths/profile.html' , {'address': address})


@login_required(login_url='login')
def user_update(request):
    if request.user.is_authenticated:
        user_info = User.objects.get(id=request.user.id)
        user_form = AccountUpdateForm(request.POST or None, instance=user_info)
        if user_form.errors:
            print(user_form.errors)
        if user_form.is_valid():
            user_form.save()
            login(request, user_info)
            messages.success(request, 'user has been updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'please recheck your Info')
        return render (request, 'auths/user.html', {'form' : user_form})
    else:
        messages.success(request, 'you need to login to be able to view this page')
        return redirect('login')

@login_required(login_url='login')
def profile_update(request):
    if request.user.is_authenticated:
        profile_info = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST or None, instance=profile_info)
        if profile_form.errors:
            print(profile_form.errors)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'user has been updated successfully')
            return redirect('profile')
        return render (request, 'auths/settings.html', {'form' : profile_form})
    else:
        messages.success(request, 'you need to login to be able to view this page')
        return redirect('login')
        
       

