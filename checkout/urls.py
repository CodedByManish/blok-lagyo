from django.urls import path, include
from . import views  

urlpatterns = [
    path('', views.checkout, name='checkout'),
    
    #Esewa 
    path('esewa-success/', views.esewa_success, name='esewa_success'),
    path('esewa-failure/', views.esewa_failure, name='esewa_failure'),

    # Khalti
    path('khalti-checkout/', views.khalti_checkout, name='khalti_checkout'),
    path('khalti-verify/', views.khalti_verify, name='khalti_verify'),  

    #PayPal
    path('paypal-checkout/', views.paypal_checkout, name='paypal_checkout'),
    path('paypal-success/', views.paypal_success, name='paypal_success'),
    path('paypal-cancel/', views.paypal_cancel, name='paypal_cancel'),

    # REQUIRED for IPN
    path('paypal/', include('paypal.standard.ipn.urls')),
]