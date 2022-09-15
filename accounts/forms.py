from django import forms
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import Address


class AddressSelectionForm(forms.Form):
    '''
    form dynamically specifies the parameters in the declared fields. In this case we are restricting addresses to the ones that are connected to the current user, thus requiring authentication.
    '''

    billing_address = forms.ModelChoiceField(queryset=None)
    shipping_address = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):

        super().__init__(*args, **kwargs)

        try:
            queryset = Address.objects.filter(user=user)
            self.fields['billing_address'].queryset = queryset
            self.fields['shipping_address'].queryset = queryset

        except Address.DoesNotExist:
            redirect('create-address')


class PaymentSelectionForm(forms.Form):
    CHOICES = (
        ('M', 'M-PESA'),
        ('C', 'Visa/MasterCard'),
        ('P', 'Paypal'),
        ('S', 'Stripe'),
    )

    method = forms.ChoiceField(
        choices=CHOICES,  label='Select payment method:')


class PeriodSelectForm(forms.Form):
    PERIODS = ((30, "30 days"), (60, "60 days"), (90, "90 days"))
    period = forms.TypedChoiceField(choices=PERIODS, coerce=int, required=True)
