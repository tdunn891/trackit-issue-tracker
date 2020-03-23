from django import forms
from .models import Order


class MakePaymentForm(forms.Form):

    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2036)]

    credit_card_number = forms.CharField(
        label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)',
                          required=False)
    expiry_month = forms.ChoiceField(
        label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(
        label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'street_address1': forms.TextInput(attrs={'placeholder': 'Street Address (line 1)'}),
            'street_address2': forms.TextInput(attrs={'placeholder': 'Street Address (line 2)'}),
            'town_or_city': forms.TextInput(attrs={'placeholder': 'Town/City'}),
            'county': forms.TextInput(attrs={'placeholder': 'County'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'})
        }
        fields = (
            'full_name', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2',
            'county'
        )
