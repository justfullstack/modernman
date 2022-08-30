import logging
from django.contrib import admin
from django.utils.html import format_html

from shop.models import CartLine, Order, OrderLine, Cart, Product, ProductImage

logger = logging.getLogger(__name__)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock_count',
                      'slug',  'price')
    list_filter = ('active',    'on_sale',  'date_uploaded')
    list_editable = ('stock_count',  'price', 'description')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",) } 

    # slug is an important field for our site, it is used in
    # all the product URLs. We want to limit the ability to
    # change this only to the owners of the company.

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    # This is required for get_readonly_fields to work
    def get_prepopulated_fields(self, request, obj):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}

    def make_active(self, request, queryset):
        """Marks selected items as active"""
        queryset.update(active=True)

    make_active.short_description = "Marks selected items as active"

    def make_inactive(self, request, queryset):
        """Marks selected items as inactive"""
        queryset.update(active=False)

    make_inactive.short_description = "Marks selected items as inactive"

    actions = [make_active, make_inactive]


class DispatchersProductAdmin(ProductAdmin):
    readonly_field = ("description", "price", "category", "active")
    list_filter = ("active", )
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name", )}

 
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    readonly_fields = ('thumbnail',)
    search_fields = ('product_name',)

    def thumbnail_tag(self, obj):
        """
        this function returns HTML for the first column defined 
        in the list_display property above

        """
        if obj.thumbnail:
            return format_html(
                f'<img src="{obj.thumbnail.url}"/>'
            )
        return "-"

    # this defines the column name for the list_display
    thumbnail_tag.short_description = "Product thumbnail"

    def product_name(self, obj):
        return obj.product.name


# For models like Cart and Order,
# which have foreign keys pointing from their relevant line model,
# we need to use an Inline to show the related data.

# visualize cartline in admin
class CartLineInline(admin.TabularInline):
    model = CartLine
    raw_id_fields = ('product', )


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status',   )
    list_editable = ('status', )
    list_filter = ('status', )
    inlines = (CartLineInline, )


# visualize orderline in admin
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    raw_id_fields = ('product', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', )
    list_editable = ('status', )
    list_filter = ('status', 'shipping_county', 'date_added', )
    inlines = (OrderLineInline, )

    fieldsets = (
        (None, {'fields':
                (
                    'user',
                    'status'
                )
                }
         ),

        ('Billing Info', {
            'fields': (
                'billing_name',
                'billing_address',
                'billing_postal_code',
                'billing_county',
                'billing_city',
                'billing_country',
                'billing_phone_no'
            )

        },
        ),


        ('Shipping Info',  {
            'fields': (
                'shipping_name',
                'shipping_address',
                'shipping_postal_code',
                'shipping_county',
                'shipping_city',
                'shipping_country',
                'shipping_phone_no'
            )

        },
        ),

    )

 

# Employees need a custom version of the order views because
# they are not allowed to change products already purchased
# without adding and removing lines

class CentralOfficeOrderInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ('product', )


class CentralOfficeOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')
    list_editable = ('status', )
    readonly_fields = ('user', )
    list_filter = ('status', 'shipping_country', 'date_added', )
    inlines = (CentralOfficeOrderInline, )

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'status'
            )
        }
        ),

        ('Billing Info', {
            'fields': (
                'billing_name',
                'billing_address',
                'billing_postal_code',
                'billing_county',
                'billing_city',
            )
        }
        ),

        ('Shippping Info', {
            'fields': (
                'shipping_name',
                'shipping_address',
                'shipping_postal_code',
                'shipping_county',
                'shipping_city',
            )
        }
        ),
    )

    # Dispatchers do not need to see billing info


class DispatchersOrderAdmin(admin.ModelAdmin):
    """
    overrides the get_queryset() method because the dispatch office only needs to see the
    orders that have been marked as 'PAID' already on which  they only need to see the shipping address.
    """
    list_display = ('id', 'shipping_name', 'date_added', 'status')
    list_filter = ('status', 'shipping_country', 'date_added', )
    inlines = (CentralOfficeOrderInline, )

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'status'
            )
        }
        ),



        ('Shippping Info', {
            'fields': (
                'shipping_name',
                'shipping_address',
                'shipping_postal_code',
                'shipping_county',
                'shipping_city',
            )
        }
        ),
    )

# Dispatchers are only allowed to see orders that
# are ready to be shipped

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=Order.PAID)





admin.site.register(Product, ProductAdmin )
admin.site.register(ProductImage, ProductImageAdmin )
admin.site.register(Cart, CartAdmin ) 