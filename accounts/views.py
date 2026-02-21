from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth import authenticate, login
from checkout.models import Order


# Index page
def index(request):
    return render(request, "index.html")


# Logout
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect(reverse('index'))


# Login view
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username_or_email=username_or_email, password=password)
            
            if user:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend',)
                messages.success(request, f"Welcome back, {user.username}!")
                # Check for 'next' parameter, otherwise go to home
                next_url = request.POST.get('next') or request.GET.get('next')
                return redirect(next_url if next_url else 'index') # Change 'index' to 'home'
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {
        'user_form': form,
        'next': request.GET.get('next', '')
    })

def logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')[:10]

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {
        'form': form,
        'orders': orders
    })


# Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful")
                return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': form})
