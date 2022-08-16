from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from shop.models import Cart, CartLine, Product, ProductTag
from django.contrib import messages


class ProductListView(ListView):

    template_name = "shop/product_list.html"
    paginate_by = 4

    def get_queryset(self):

        tag = self.kwargs['tag']

        # get tag from link
        if tag == "all" or tag == "":
            self.tag = None
        else:
            self.tag = get_object_or_404(ProductTag, slug=tag)

        # use tag (if any) to retreive data
        if self.tag is not None:
            products = Product.objects.active().filter(tags=self.tag)
        else:
            products = Product.objects.active()

        return products.order_by("name")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'


# add to cart
def addToCart(request):
    '''
    adds a product to the cart,  relying on 
    the cart_middleware to position the existing
    basket inside the request.basket attribute
    '''
    product_id = request.GET.get("product_id")

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    cart = request.cart

# if cart doesn't exist create one
    if not cart:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        cart = Cart.objects.create(user=user)

        request.session["cart_id"] = cart.id

    (cartline, created) = CartLine.objects.get_or_create(
        cart=cart, product=product)

    # if cart was already initiated
    if not created:

        cartline.quantity += 1
        cartline.save()
 

    messages.success(
        request, f"{product.name.title()} successfully added to the cart!")

    # return

    return redirect(
        reverse(
            "product",
            args=(product.slug,)
        )
    )
