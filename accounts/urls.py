
from django.urls import path
from .views import AddressCreateView, AddressDeleteView, AddressUpdateView, AddressListView, AddressSelectionView

urlpatterns = [
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

        path(
            'update-address/',
            AddressUpdateView.as_view(),
            name="update-address"
        ),

        path(
            'delete-address/',
            AddressDeleteView.as_view(),
            name="delete-address"
        ),

        path(
            'select-address/',
            AddressSelectionView.as_view(),
            name="select-address"
        ),

        path(
            'addresses/',
            AddressListView.as_view(),
            name="list_address"
        ),
        ]