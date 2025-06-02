from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate

# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {'error': 'Username or email is already in use'})

        if password1:
            user = User.objects.create_user(
                username, 
                email, 
                password1,
                first_name = request.POST['first_name'], 
                last_name = request.POST['last_name']
            )
            user.save()

            user_profile, created = Profile.objects.get_or_create(user=user)
            # user_profile.phone_number = phone_number
            user_profile.save()

            return redirect('dashboard')
        else:
            return render(request, 'users/register.html', {'error': 'Unable to create account'})
    return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Incorrect username or password'})
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def settings(request):
    user = request.user
    user_profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user_profile.phone = request.POST['phone_number']
        user_profile.avatar = request.FILES.get('avatar')
        
        if user_profile.starting_balance is None or user_profile.starting_balance == 0:
            user_profile.starting_balance = request.POST['starting_balance']
        
        user.save()
        user_profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')
        
    context = {
        'username': request.user.username,
        'user': user, 
        'user_profile': user_profile,
        'current_path': request.path,
    }
    return render(request, 'users/settings.html', context)