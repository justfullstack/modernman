
from django.urls import path
from .views import AddressCreateView, AddressDeleteView, AddressUpdateView, AddressListView, AddressSelectionView


path(
    'create-address/',
    AddressCreateView.as_view(),
    name="create-address"
),

path(
    'select-address/',
    AddressSelectionView.as_view(),
    name="select-address"
),
