from django.urls import path, include
from . import urls_reset
from .views import index, register, profile, logout, login

app_name = 'accounts' 

urlpatterns = [ # This is now 'accounts: '
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'), 
    path('password-reset/', include('accounts.urls_reset')),
    path('', index, name='index'),
]