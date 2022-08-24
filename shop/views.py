from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from accounts.models import Address
from shop.forms import AddressSelectionForm, CartLineFormSet
from shop.models import Cart, CartLine, Product, ProductTag
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(ListView):

    template_name = "shop/product_list.html"
    paginate_by = 4

    def get_queryset(self):

        tag = self.kwargs['tag']

        # get tag from link
        if tag == "all" or tag == "":
            self.tag = None
            products = Product.objects.active()
        else:
            self.tag = get_object_or_404(ProductTag, slug=tag)

        # use tag (if any) to retreive data
        if self.tag is not None:
            products = Product.objects.active().filter(tags=self.tag)

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
        # if product already in cart, do nothing
        # send message
        messages.error(
            request, f"'{product.name.title().strip('.')}' already in the cart!")
    else:
        cart.count += cart.cartline_set.all().count()
        cart.save()
        cartline.save()

        messages.success(
            request, f"'{product.name.title().strip('.')}' successfully added to the cart!")

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


#########################  SHIPPING: ADDRESSES CRUD VIEWS  ###########################
class AddressSelectionView(LoginRequiredMixin, FormView):

    template_name = 'shop/select_address.html'
    form_class = AddressSelectionForm
    success_url = reverse_lazy('checkout-done')

    def get_form_kwargs(self):
        '''extracts the user from the request and returns it in a dictionary - dictionary is then passed to the form by the superclass'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # delete the cart from the session
        del self.request.session['cart_id']

        # create order with the submitted addresses data
        cart = self.request.cart
        cart.createOrder(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )

        return super().form_valid(form)


class AddressListView(LoginRequiredMixin, ListView):
    model = Address

    def get_queryset(self):
        return self.model.objects.get(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['address', 'postal_code', ' town',
              'county', 'city', 'country', 'phone_no']


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = '__all__'


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
