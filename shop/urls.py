
from django.urls import path
from .views import ProductListView, ProductDetailView, addToCart, manageCart

urlpatterns = [


    path(
        "product/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product",
    ),

    path(
        'add-to-cart',
        addToCart,
        name='add-to-cart'
    ),

    path(
        'cart/',
        manageCart,
        name="basket"
    ),

    # path(
    #     'checkout-done/',
    #     completeCheckout, # change
    #     name="checkout-done"
    #     ),

    # path(
    #     'create-address/',
    #     AddressCreateView.as_view(),
    #     name="create-address"
    #     ),

    # path(
    #     'select-address/',
    #     AddressSelectionView.as_view(),
    #     name="select-address"
    #     ),

    # path(
    #     'complete-order/',
    #     TemplateView.as_view(template_name='shop/complete-order.html'),
    #     name="checkout-done"
    #     ),

    path(
        '<slug:tag>/',
        ProductListView.as_view(),
        name='products'
    ),



]
