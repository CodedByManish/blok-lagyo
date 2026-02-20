fooddelivery/settings:
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'  # replace with your secret key

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'accounts',
    'products',
    'cart',
    'checkout',
    'home',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fooddelivery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'cart.contexts.cart_contents',
            ],
        },
    },
]

WSGI_APPLICATION = 'fooddelivery.wsgi.application'

# ---- DATABASE (SQLite) ----
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.CaseInsensitiveAuth',
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static & Media (local)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTH_USER_MODEL = 'accounts.CustomUser'

# eSewa settings
#ESEWA_RETURN_URL = 'http://


fooddelivery/urls:
"""Food delivery app URL configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # authentication
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # app urls
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
]

# media files (dev only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








accounts/admin:

# Username: admin
# Email address: abc@123.com
# Password: 1234

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'profile_picture', 'address'),
        }),
    )



accounts/admin:
from django.apps import AppConfig
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


accounts/backends:
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CaseInsensitiveAuth:
    """
    Authenticate using username OR email (case-insensitive)
    """

    def authenticate(self, request, username_or_email=None, password=None):
        if username_or_email is None or password is None:
            return None

        try:
            user = User.objects.get(
                Q(username__iexact=username_or_email) |
                Q(email__iexact=username_or_email)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



accounts/foms:
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email



accounts/models:
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username



accounts/urls_reset:
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.PasswordResetView.as_view(
        success_url='/accounts/password-reset/done/'), name='password_reset'),
    path('done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url='/accounts/password-reset/complete/'), name='password_reset_confirm'),
    path('complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



accounts/urls:
from django.urls import path, include
from . import urls_reset
from .views import index, register, profile, logout, login

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('password-reset/', include(urls_reset)),
    path('', index, name='index'),
]




accounts/views:
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm


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

            user = auth.authenticate(
                request,
                username_or_email=username_or_email,
                password=password
            )

            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in")
                next_url = request.GET.get('next')
                return redirect(next_url or 'index')
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {
        'user_form': form,
        'next': request.GET.get('next', '')
    })


# Profile
@login_required
def profile(request):
    return render(request, 'profile.html')


# Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, "Registration successful")
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'user_form': form})




accounts/templates/registration/password_reset_complete.html
{% extends "base.html" %}
{% block title %}Password Reset Complete{% endblock %}

{% block content %}
<h2>Password Reset Complete</h2>
<p>Your password has been set. You may now log in with your new password.</p>
<p><a href="{% url 'login' %}" class="btn btn-primary">Log in</a></p>
{% endblock %}


accounts/templates/registration/password_reset_confirm.html
{% extends "base.html" %}
{% block title %}Set New Password{% endblock %}

{% block content %}
<h2>Set a New Password</h2>

{% if validlink %}
<form method="post" class="accountform">
    {% csrf_token %}

    <div class="form-group">
        {{ form.new_password1.label_tag }}
        {{ form.new_password1 }}
        {{ form.new_password1.errors }}
    </div>

    <div class="form-group">
        {{ form.new_password2.label_tag }}
        {{ form.new_password2 }}
        {{ form.new_password2.errors }}
    </div>

    <button type="submit" class="btn btn-success">
        Change my password
    </button>
</form>
{% else %}
<h3>Password reset unsuccessful</h3>
<p>
    The password reset link was invalid, possibly because it has already been used.
    Please request a new password reset.
</p>
{% endif %}
{% endblock %}



accounts/templates/registration/password_reset_delete.html
{% extends "base.html" %}
{% block title %}Password reset successful{% endblock %}
{% block content %}
<h2>Password Reset Sent</h2>
<p>We've emailed you instructions for setting your password to the email address you submitted.</p>
<p>Please check your inbox shortly.</p>
{% endblock %}




accounts/templates/registration/password_reset_email.html
{% autoescape off %}
You're receiving this email because you requested a password reset for your user account at {{ site_name }}.
Please go to the following page and choose a new password:
{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
Your username, in case you've forgotten: {{ user.username }}
Thanks for using our site!

The {{ site_name }} team.
{% endautoescape %}




accounts/templates/registration/password_reset_form.html
{% extends "base.html" %}
{% block title %}Reset Password{% endblock %}

{% block content %}
<h2>Reset Your Password</h2>
<p>Please enter your email address to receive instructions for resetting your password.</p>

<form method="post" class="accountform">
    {% csrf_token %}
    {{ form.email.errors }}
    <p>
        <label for="id_email" class="control-label required-field">E-mail address:</label>
        {{ form.email }}
    </p>
    <p><input type="submit" value="Reset Password" class="btn btn-primary"/></p>
</form>
{% endblock %}




accounts/templates/index.html
{% extends "base.html" %}
{% load static %}

{% block title %}Home{% endblock %}

{% block content %}
<div class="container" style="margin-top: 80px;">
    <div class="jumbotron text-center">
        <h1>Welcome to Bhok Lagyo!</h1>
        <p>Your favorite sushi delivered fast and fresh.</p>
        {% if user.is_authenticated %}
            <p>Hello, {{ user.username }}!</p>
            <a href="{% url 'products' %}" class="btn btn-success btn-lg">
                <i class="fa fa-cutlery"></i> View Menu
            </a>
        {% else %}
            <a href="{% url 'login' %}" class="btn btn-primary btn-lg">
                <i class="fa fa-sign-in"></i> Log In
            </a>
            <a href="{% url 'register' %}" class="btn btn-success btn-lg">
                <i class="fa fa-user-plus"></i> Register</a>
        {% endif %}
    </div>

    <div class="row text-center" style="margin-top: 50px;">
        <div class="col-md-4">
            <i class="fa fa-truck fa-3x"></i>
            <h3>Fast Delivery</h3>
            <p>Get your food delivered hot and fresh in no time.</p>
        </div>
        <div class="col-md-4">
            <i class="fa fa-leaf fa-3x"></i>
            <h3>Fresh Ingredients</h3>
            <p>Only the finest ingredients for a premium taste experience.</p>
        </div>
        <div class="col-md-4">
            <i class="fa fa-star fa-3x"></i>
            <h3>Quality Service</h3>
            <p>Enjoy hassle-free ordering with a smooth and friendly service.</p>
        </div>
    </div>
</div>
{% endblock %}







accounts/templates/login.html
{% extends "base.html" %}
{% load static %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="container" style="max-width: 400px; margin-top: 50px;">
    <h2 class="text-center">Login</h2>
    <hr>
    <form method="post">
        {% csrf_token %}
        {{ user_form.non_field_errors }}

        <div class="form-group">
            {{ user_form.username_or_email.label_tag }}
            {{ user_form.username_or_email }}
            {{ user_form.username_or_email.errors }}
        </div>

        <div class="form-group">
            {{ user_form.password.label_tag }}
            {{ user_form.password }}
            {{ user_form.password.errors }}
        </div>

        <input type="hidden" name="next" value="{{ next }}">
        <button type="submit" class="btn btn-success btn-block">Login</button>
    </form>
    <p class="text-center" style="margin-top: 10px;">
        Don't have an account? <a href="{% url 'register' %}">Register here</a>
    </p>
    <p class="text-center">
        <a href="{% url 'password_reset' %}">Forgot your password?</a>
    </p>
</div>
{% endblock %}




accounts/templates/profile
{% extends "base.html" %}
{% load static %}

{% block title %}My Profile{% endblock %}

{% block content %}
<div class="container" style="max-width: 600px; margin-top: 50px;">
    <h2 class="text-center">My Profile</h2>
    <hr>

    <div class="panel panel-default">
        <div class="panel-heading"><strong>Account Information</strong></div>
        <div class="panel-body">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>First Name:</strong> {{ user.first_name }}</p>
            <p><strong>Last Name:</strong> {{ user.last_name }}</p>
        </div>
    </div>

    <div class="text-center" style="margin-top: 20px;">
        <a href="{% url 'logout' %}" class="btn btn-danger"><i class="fa fa-sign-out"></i> Log Out</a>
        <a href="{% url 'index' %}" class="btn btn-primary"><i class="fa fa-home"></i> Home</a>
    </div>
</div>
{% endblock %}



accounts/templates/register.html
{% extends "base.html" %}
{% load static %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="container" style="max-width: 500px; margin-top: 50px;">
    <h2 class="text-center">Create an Account</h2>
    <hr>
    <form method="post">
        {% csrf_token %}
        {{ user_form.non_field_errors }}
        <div class="form-group">
            {{ user_form.username.label_tag }}
            {{ user_form.username }}
            {{ user_form.username.errors }}
        </div>
        <div class="form-group">
            {{ user_form.email.label_tag }}
            {{ user_form.email }}
            {{ user_form.email.errors }}
        </div>
        <div class="form-group">
            {{ user_form.password1.label_tag }}
            {{ user_form.password1 }}
            {{ user_form.password1.errors }}
        </div>
        <div class="form-group">
            {{ user_form.password2.label_tag }}
            {{ user_form.password2 }}
            {{ user_form.password2.errors }}
        </div>
        <button type="submit" class="btn btn-primary btn-block">Register</button>
    </form>
    <p class="text-center" style="margin-top: 10px;">
        Already have an account? <a href="{% url 'login' %}">Log in</a>
    </p>
</div>
{% endblock %}







FOR HOME
home/apps.py:
from django.apps import AppConfig
class HomeConfig(AppConfig):
    name = 'home'

home/views:
from django.shortcuts import render
def index(request):
    return render(request, "home/index.html")

home/templates/home.html:
{% extends 'base.html' %}

{% block content %}

<div class="row">
    <div class="col-md-4"></div>

    <div class="col-md-4 text-center">
        <p>
            Welcome to <strong>Blog-Lagyo</strong> — your go-to food delivery app in Nepal.
            We bring you fresh, delicious meals and authentic sushi straight to your doorstep.
            Create an account, log in, and explore our menu to discover special offers and local favorites.
            <br><br>
            Enjoy your meal! 
        </p>
    </div>

    <div class="col-md-4"></div>
</div>

<div class="index-banner text-center">
    <img
        class="featurette-image img-responsive"
        src="https://s3.eu-central-1.amazonaws.com/food-delivery-app/static/images/banner1.jpg"
        alt="Blog-Lagyo food delivery banner">
</div>

{% endblock %}




FOR PRODUCTS,
products/apps:from django.contrib import admin
from .models import Product
admin.site.register(Product)


products/models:
from django.db import models
from django.utils import timezone
class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(default=timezone.now)  # <--- default for existing rows
    def __str__(self):
        return self.name


products/urls:
from django.urls import path
from .views import all_products, product_detail

urlpatterns = [
    path('', all_products, name='products'),
    path('<int:pk>/', product_detail, name='product_detail'),
]



products/views:
from django.shortcuts import render, get_object_or_404
from .models import Product
# List of all products
def all_products(request):
    products = Product.objects.filter(available=True)
    return render(request, "products/product_list.html", {"products": products})
# Product detail page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, "products/product_detail.html", {"product": product})


products/templates/product_details.html
{% extends 'base.html' %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            {% if product.image %}
            <img src="{{ product.image.url }}" class="img-fluid" alt="{{ product.name }}">
            {% endif %}
        </div>
        <div class="col-md-6">
            <h2>{{ product.name }}</h2>
            <p>{{ product.description }}</p>
            <p>Price: €{{ product.price }}</p>
            <a href="{% url 'cart_add' product.id %}" class="btn btn-success">Add to Cart</a>
        </div>
    </div>
</div>
{% endblock %}


products/templates/product_list.html:
{% extends 'base.html' %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            {% if product.image %}
            <img src="{{ product.image.url }}" class="img-fluid" alt="{{ product.name }}">
            {% endif %}
        </div>
        <div class="col-md-6">
            <h2>{{ product.name }}</h2>
            <p>{{ product.description }}</p>
            <p>Price: €{{ product.price }}</p>
            <a href="{% url 'cart_add' product.id %}" class="btn btn-success">Add to Cart</a>
        </div>
    </div>
</div>
{% endblock %}






FOR CART,
cart/templates/cart.html:
{% extends 'base.html' %}

{% block title %}Your Cart{% endblock %}

{% block content %}
<h2 class="text-center mt-4">Your Cart</h2>
{% if cart_items %}
<table class="table table-bordered mt-3">
    <thead>
        <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Subtotal</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        {% for item in cart_items %}
        <tr>
            <td>{{ item.product.name }}</td>
            <td>€{{ item.product.price }}</td>
            <td>
                <form method="post" action="{% url 'adjust_cart' item.id %}">
                    {% csrf_token %}
                    <input type="number" name="quantity" value="{{ item.quantity }}" min="0" class="form-control" style="width: 80px;">
                    <button type="submit" class="btn btn-sm btn-primary mt-1">Update</button>
                </form>
            </td>
            <td>€{{ item.subtotal }}</td>
            <td>
                <form method="post" action="{% url 'adjust_cart' item.id %}">
                    {% csrf_token %}
                    <input type="hidden" name="quantity" value="0">
                    <button type="submit" class="btn btn-sm btn-danger">Remove</button>
                </form>
            </td>
        </tr>
        {% endfor %}
        <tr>
            <td colspan="3" class="text-right"><strong>Total:</strong></td>
            <td colspan="2">€{{ total }}</td>
        </tr>
    </tbody>
</table>
<a href="{% url 'checkout' %}" class="btn btn-success">Proceed to Checkout</a>
{% else %}
<p class="text-center mt-3">Your cart is empty. <a href="{% url 'products' %}">Continue shopping</a>.</p>
{% endif %}
{% endblock %}


cart/apps.py:
from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'cart'


cart/contexts.py:
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    """
    Makes cart contents available in all templates.
    """
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = quantity * product.price
        cart_items.append({
            'id': product.id,
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
        product_count += quantity

    return {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }


cart/models.py: <nothing>


cart/views.py:
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from products.models import Product

# View cart page
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': quantity * product.price
        })
        total += quantity * product.price

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, "cart/cart.html", context)

# Add item to cart
def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + quantity
    request.session['cart'] = cart

    return redirect(reverse('products'))

# Adjust quantity or remove item
def adjust_cart(request, id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        cart[str(id)] = quantity
    else:
        cart.pop(str(id), None)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


cart/urls.py:
from django.urls import path
from .views import view_cart, add_to_cart, adjust_cart

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<int:id>/', add_to_cart, name='add_to_cart'),
    path('adjust/<int:id>/', adjust_cart, name='adjust_cart'),
]




FOR CHECKOUT,
checkout/admin:
from django.contrib import admin
from .models import Order, OrderLineItem
class OrderLineAdminInline(admin.TabularInline):
    model = OrderLineItem
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline, )
admin.site.register(Order, OrderAdmin)  


checkout/apps:
from django.apps import AppConfig
class CheckoutConfig(AppConfig):
    name = 'checkout'


checkout/esewa.py:
import hmac
import hashlib
import base64

class eSewa:
    def __init__(self, secret_key="8gBm/:&EnhH.1/q", product_code="EPAYTEST"):
        self.secret_key = secret_key.encode()
        self.product_code = product_code

    def generate_signature(self, total_amount, transaction_uuid):
        """
        Generates HMAC SHA256 signature for a payment
        """
        message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={self.product_code}"
        signature = hmac.new(self.secret_key, message.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()


checkout/forms.py:
from django import forms
from .models import Order

class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2019, 2036)]
    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2',
            'county'
)


checkout/models:
from django.db import models
from products.models import Product

class Order(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    county = models.CharField(max_length=40, blank=False)
    date = models.DateField()

    def __str__(self):
        return f"{self.id}-{self.date}-{self.full_name}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    def __str__(self):
        return f"{self.quantity} {self.product.name} @ {self.product.price}"


checkout/urls:
from django.urls import path
from .views import checkout, esewa_success, esewa_failure
urlpatterns = [
    path('', checkout, name='checkout'),
    path('esewa-success/', esewa_success, name='esewa_success'),
    path('esewa-failure/', esewa_failure, name='esewa_failure'),
]


checkout/views.py:
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
from .esewa import eSewa

@login_required
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()

            # Generate HMAC signature
            esewa_helper = eSewa()
            transaction_uuid = str(order.id)
            signature = esewa_helper.generate_signature(total, transaction_uuid)

            # Redirect to eSewa
            esewa_url = "https://uat.esewa.com.np/epay/main"
            data = {
                'tAmt': total,
                'amt': total,
                'txAmt': 0,
                'psc': 0,
                'pdc': 0,
                'scd': esewa_helper.product_code,
                'pid': transaction_uuid,
                'su': settings.ESEWA_RETURN_URL,
                'fu': settings.ESEWA_CANCEL_URL,
                'signature': signature,  # custom param
            }

            return render(request, "redirect_esewa.html", {'esewa_url': esewa_url, 'data': data})
    else:
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form': order_form})


@login_required
def esewa_success(request):
    order_id = request.GET.get('pid')  # eSewa returns pid
    ref_id = request.GET.get('refId')
    amount = request.GET.get('amt')
    order = get_object_or_404(OrderLineItem, order__id=order_id).order
    esewa_helper = eSewa()
    expected_signature = esewa_helper.generate_signature(float(amount), str(order_id))
    received_signature = request.GET.get('signature')
    if received_signature == expected_signature:
        messages.success(request, "Payment successful via eSewa!")
        request.session['cart'] = {}
    else:
        messages.error(request, "Payment verification failed. Signature mismatch.")
    return redirect(reverse('products'))
@login_required
def esewa_failure(request):
    messages.error(request, "Payment failed or cancelled via eSewa!")
    return redirect(reverse('checkout'))

checkout/templates/checkout.html:
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
from .esewa import eSewa

@login_required
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()

            # Generate HMAC signature
            esewa_helper = eSewa()
            transaction_uuid = str(order.id)
            signature = esewa_helper.generate_signature(total, transaction_uuid)

            # Redirect to eSewa
            esewa_url = "https://uat.esewa.com.np/epay/main"
            data = {
                'tAmt': total,
                'amt': total,
                'txAmt': 0,
                'psc': 0,
                'pdc': 0,
                'scd': esewa_helper.product_code,
                'pid': transaction_uuid,
                'su': settings.ESEWA_RETURN_URL,
                'fu': settings.ESEWA_CANCEL_URL,
                'signature': signature,  # custom param
            }

            return render(request, "redirect_esewa.html", {'esewa_url': esewa_url, 'data': data})
    else:
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form': order_form})


@login_required
def esewa_success(request):
    order_id = request.GET.get('pid')  # eSewa returns pid
    ref_id = request.GET.get('refId')
    amount = request.GET.get('amt')
    order = get_object_or_404(OrderLineItem, order__id=order_id).order
    esewa_helper = eSewa()
    expected_signature = esewa_helper.generate_signature(float(amount), str(order_id))
    received_signature = request.GET.get('signature')
    if received_signature == expected_signature:
        messages.success(request, "Payment successful via eSewa!")
        request.session['cart'] = {}
    else:
        messages.error(request, "Payment verification failed. Signature mismatch.")
    return redirect(reverse('products'))
@login_required
def esewa_failure(request):
    messages.error(request, "Payment failed or cancelled via eSewa!")
    return redirect(reverse('checkout'))


    meanwhile , my project directory is : "(env) F:\blok lagyo" where the base.html: {% load static %} <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>{% block title %}Bhok Lagyo{% endblock %}</title> <!-- Bootstrap CSS --> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> <!-- Font Awesome --> <link rel="stylesheet" href="{% static 'font-awesome/css/font-awesome.min.css' %}"> <!-- Custom CSS --> <link rel="stylesheet" href="{% static 'css/custom.css' %}"> {% block head_js %}{% endblock head_js %} </head> <body> <!-- Navbar --> <nav class="navbar navbar-default navbar-fixed-top"> <div class="container"> <!-- Brand and toggle --> <div class="navbar-header"> <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse"> <span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span> </button> <a class="navbar-brand" href="{% url 'index' %}">Bhok Lagyo</a> </div> <!-- Navbar links --> <div class="collapse navbar-collapse" id="navbar-collapse"> <ul class="nav navbar-nav navbar-right"> {% if user.is_authenticated %} <li><a href="{% url 'profile' %}"><i class="fa fa-user"></i> {{ user.username }}</a></li> <li><a href="{% url 'products' %}"><i class="fa fa-cutlery"></i> Menu</a></li> <li> <a href="{% url 'view_cart' %}"> <i class="fa fa-shopping-cart"></i> Cart {% if request.session.cart %} <span class="badge">{{ request.session.cart|length }}</span> {% endif %} </a> </li> <li><a href="{% url 'logout' %}"><i class="fa fa-sign-out"></i> Logout</a></li> {% else %} <li><a href="{% url 'login' %}"><i class="fa fa-sign-in"></i> Login</a></li> <li><a href="{% url 'register' %}"><i class="fa fa-user-plus"></i> Register</a></li> {% endif %} </ul> </div> </div> </nav> <!-- Messages --> <div class="container" style="margin-top: 70px;"> {% if messages %} {% for message in messages %} <div class="alert alert-{{ message.tags }} alert-dismissible" role="alert"> <button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button> {{ message }} </div> {% endfor %} {% endif %} </div> <!-- Main content --> <div class="container"> {% block content %}{% endblock %} </div> <!-- Footer --> <footer class="container-fluid text-center" style="margin-top: 50px; padding: 20px; background-color: #f5f5f5;"> <p>&copy; {{ now|date:"Y" }} Bhok Lagyo. All rights reserved.</p> <p>Follow us on <a href="https://twitter.com" target="_blank"><i class="fa fa-twitter"></i></a> <a href="https://instagram.com" target="_blank"><i class="fa fa-instagram"></i></a> <a href="https://youtube.com" target="_blank"><i class="fa fa-youtube"></i></a> </p> </footer> <!-- jQuery & Bootstrap JS --> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> {% block extra_js %}{% endblock %} </body> </html>