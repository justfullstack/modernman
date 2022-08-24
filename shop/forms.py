# formset will automatically build forms for all basket lines
# connected to the basket specified;
# only editable fields will be quantity and there will be no extra form to add new entries
# that done  through the add_to_cart view


from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from shop.models import Cart, CartLine
from accounts.models import Address

CartLineFormSet = inlineformset_factory(
    Cart,
    CartLine,
    fields=("quantity",),
    extra=0,
    #widgets={"quantity": widgets.PlusMinusWidget()},
)


class AddressSelectionForm(forms.Form):
    '''
    form dynamically specifies the parameters in the declared fields. In this case we are restricting addresses to the ones that are connected to the current user.
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
