from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import path, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.template.loader import render_to_string
from weasyprint import HTML
from shop.models import Order
from .forms import AddressSelectionForm
from accounts.models import Address
import tempfile
# Create your views here.

#########################  SHIPPING: ADDRESSES ###########################


class AddressSelectionView(LoginRequiredMixin, FormView):

    template_name = 'accounts/select_address.html'
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
    template_name = 'accounts/address_list.html'

    def get_queryset(self):
        return self.model.objects.get(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'accounts/address_form.html'
    fields = ['address', 'postal_code', ' town',
              'county', 'city', 'country', 'phone_no']


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/address_update.html'
    model = Address
    fields = '__all__'


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/confirm_delete.html'
    model = Address


############################# generate invoice #########################
class InvoiceMixin:
    """
    This mixin will be used for the invoice functionality, which is only available to owners and employees, but not dispatchers
    """

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path(
                "invoice/<int:order_id>/",
                self.admin_view(self.generateInvoiceForOrder),
                name="invoice",
            )
        ]
        return my_urls + urls

    def generateInvoiceForOrder(self, request, order_id):
        """
        This  view has two rendering modes, HTML and PDF. 
        Both modes use the same invoice.html template, but in the case of PDF,
        WeasyPrint is used to post-process the output of the templating engine.
        """

        order = get_object_or_404(Order, pk=order_id)

        if request.GET.get("format") == "pdf":

            html_string = render_to_string("invoice.html",  {"order": order})

            html = HTML(string=html_string,
                        base_url=request.build_absolute_uri(), )

            result = html.write_pdf()

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f"inline; filename=invoice_{order_id}.pdf"
            response["Content-Transfer-Encoding"] = "binary"

            with tempfile.NamedTemporaryFile(delete=True) as outfile:
                outfile.write(result)


                with open(outfile.name, "rb") as out_file:
                    binary_pdf = out_file.read()
                    response.write(binary_pdf)

                outfile.flush()

            return response
        return render(request, "shop/invoice.html", {"order": order})
