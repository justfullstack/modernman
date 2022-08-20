from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from accounts.models import Address
# Create your views here.

#########################  SHIPPING: ADDRESSES ###########################


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
