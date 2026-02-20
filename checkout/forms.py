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
            'full_name', 
            'phone_number', 
            'town_or_city', 
            'street_address',
        )
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '98XXXXXXXX'}),
            'town_or_city': forms.TextInput(attrs={'placeholder': 'e.g. Birtamod,Jhapa'}),
            'street_address': forms.TextInput(attrs={'placeholder': 'Street, Ward No...'}),
        }