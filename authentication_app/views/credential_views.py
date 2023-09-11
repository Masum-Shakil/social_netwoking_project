from django.shortcuts import render, redirect
from authentication_app.models import profile_models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Please provide the valid username and password.")
            return redirect('login')
    
    return render(request, 'authentication_app/login.html')

def sign_up_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        profile = profile_models.Profile(user=user)
        profile.save()
        messages.success(request, "Congratulations!! You have signedup successfully.")
        return redirect('login')

    return render(request, 'authentication_app/signup.html')

def custom_logout(request):
    logout(request)
    return redirect('login')