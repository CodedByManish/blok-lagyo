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
