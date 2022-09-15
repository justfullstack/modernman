
from django.urls import path
from .views import AddressCreateView, AddressDeleteView, AddressUpdateView, AddressListView, AddressSelectionView, PaymentSelectionView

urlpatterns = [
    path(
        'addresses/create/',
        AddressCreateView.as_view(),
        name="create-address"
    ),


    path(
        'addresses/<int:pk>/update/',
        AddressUpdateView.as_view(),
        name="update-address"
    ),

    path(
        'addresses/<int:pk>/delete/',
        AddressDeleteView.as_view(),
        name="delete-address"
    ),

    path(
        'addresses/select/',
        AddressSelectionView.as_view(),
        name="select-address"
    ),

    path(
        'payment/select-payment/',
        PaymentSelectionView.as_view(),
        name="select-payment"
    ),

    path(
        'addresses/',
        AddressListView.as_view(),
        name="address-list"
    ),
]
