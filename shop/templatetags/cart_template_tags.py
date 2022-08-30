from django import template  
from shop.models import Cart, CartLine 


register = template.Library()


@register.filter
def cart_items_count(user):

	if user.is_authenticated:
		user = user
	else:
		user = None


	cart_qs = Cart.objects.filter(user=user) 


	if cart_qs.exists():
		cart = cart_qs[0]
		cartline_qs = CartLine.objects.filter(cart=cart)
		return cartline_qs.count()
		#return cart.cartline_set.all().count()
	else:
		return 0