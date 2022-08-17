# formset will automatically build forms for all basket lines
# connected to the basket specified;
# only editable fields will be quantity and there will be no extra form to add new entries
# that done  through the add_to_cart view


from django.forms import inlineformset_factory
from shop.models import Cart, CartLine


CartLineFormSet = inlineformset_factory(
    Cart,
    CartLine,
    fields=("quantity",),
    extra=0,
    #widgets={"quantity": widgets.PlusMinusWidget()},
)
