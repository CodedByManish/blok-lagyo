from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, email=email, password=password)
            
            if user:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome back!")
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'user_form': form})       

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
            # Explicitly specify the backend string here
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful!")
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': form})