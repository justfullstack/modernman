from django.contrib import admin

from accounts.models import Address

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    model = Address

    list_display = (
        'user',
        'name',
        'address',
        'county',
        'city',
        'country',
        'phone_no',
    )

    readonly_fields = ('user', )
