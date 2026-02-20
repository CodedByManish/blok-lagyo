from django.urls import path
from . import views  

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('esewa-success/', views.esewa_success, name='esewa_success'),
    path('esewa-failure/', views.esewa_failure, name='esewa_failure'),
    path('khalti-checkout/', views.khalti_checkout, name='khalti_checkout'),
    path('khalti-verify/', views.khalti_verify, name='khalti_verify'),
]