from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from accounts.models import Address 
from shop.models import Cart, CartLine, Product , Order 
from shop.forms import CartLineFormSet
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(ListView):

    template_name = "shop/product_list.html"
    paginate_by = 15

    def get_queryset(self):

        tag = self.kwargs['tag']

        # get tag from link
        if tag == "all" or tag == "":
            self.tag = None
            products = Product.objects.active()
        else:
            self.tag = tag

        # use tag (if any) to retreive data
        if self.tag is not None:
            products = Product.objects.active().filter(category=self.tag)

        return products.order_by("name")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'


# # add to cart
# def addToCart(request, slug): 
#     if request.user.is_authenticated:
#         user = request.user
#     else:
#         user = None


#     item = get_object_or_404(Product, slug=slug)

#     order_item = OrderItem.objects.create(user=user,item=item,status=OrderItem.OPEN)
#     order_qs = Order.objects.filter(user=user, status=Order.NEW)

#     if order_qs.exists():
#         order = order_qs[0]

#         # check if item already in order
#         # if yes, increment by 1

#         if order.items.filter(item__slug=item.slug).exists():

#             order_item.quantity += 1
#             messages.info(request, f"{product_item.name} already in the cart! ")
#             messages.success(request, f"{order_item.quantity} {item.name} now in the cart! ")
#             order_item.save()

#         else:
#             order.items.add(order_item)
#             messages.success(request, f"Successfully added to the cart!")
#     else: 
#         order = Order.objects.create(user=user )
#         order.items.add(order_item)

    
#         messages.success(request, f"Successfully added to the cart!")

#     return redirect('product', slug=slug)



# add to cart
def addToCart(request, slug):
    '''
    adds a product to the cart,  relying on 
    the cart_middleware to position the existing
    basket inside the request.basket attribute
    '''
    #product_slug = request.GET.get("product_slug")

    product = get_object_or_404(
                            Product,
                            slug=slug
                            )

    cart = request.cart

    if not cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        
    
        cart = Cart.objects.create(user=user)

        request.session["cart_id"] = cart.id

        cart.save()

            
    (cartline, created) = CartLine.objects.get_or_create(
                                            cart=cart, 
                                            product=product
                                            )

    # if cartline was already initiated
    if not created:
        messages.warning(request, f"'{product.name}' already in the cart!")

        cartline.quantity += 1
        messages.info(request, f" Item quantity updated to {cartline.quantity}!")
        cartline.save()
    else:
    
        messages.success(request, f"'{product.name}' successfully added to the cart!")

    return redirect("product",  slug=product.slug )



# remove from cart 
def removeFromCart(request, slug): 

    '''
    adds a product to the cart,  relying on 
    the cart_middleware to position the existing
    basket inside the request.basket attribute
    '''
    #product_slug = request.GET.get("product_slug")

    product = get_object_or_404(
                            Product,
                            slug=slug
                            )

    cart = request.cart

      
    cartline = CartLine.objects.filter(
                                    cart=cart, 
                                    product=product
                                    )

    # if cartline was already initiated
    if not cartline.exists():
        messages.error(request, f"'{product.name}' already in the cart!") 
    else:
        cartline.delete()
        #cartline.save()
        messages.error(request, f"'{product.name}' successfully removed from the cart!")

    return redirect("cart" )



    
    messages.error(
        request, f"'{product.name.title().strip('.')}' successfully removed from the cart!")

    return redirect(reverse("cart"))


def manageCart(request):
    if not request.cart:
        return render(request, "shop/cart.html", {"formset": None})

    # submission will be handled when the form is submitted
    # through a POST request
    if request.method == "POST":
        # process form
        formset = CartLineFormSet(request.POST,  instance=request.cart)
        if formset.is_valid():
            formset.save()
    else:
        # GET
        formset = CartLineFormSet(instance=request.cart)

    # render no formset if the user does not have a cart yet
    # or has one but it is empty
    if request.cart.is_empty():
        return render(request, "shop/cart.html", {"formset": None})

    return render(request, "shop/cart.html", {"formset": formset})


def completeCheckout(request):
    return render(request, 'shop/complete_order.html')

