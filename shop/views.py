from random import random
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from shop.models import Product, ProductTag 


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
