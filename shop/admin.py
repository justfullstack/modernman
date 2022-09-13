import logging
from django.contrib import admin
from django.utils.html import format_html
from customauth.admin import CustomUserAdmin

from customauth.models import CustomUser

from . import models

logger = logging.getLogger(__name__)


class ProductAdmin(admin.ModelAdmin):

    fieldsets = (



        ('Product Details', {
            'fields': (
                'stock_count',
                'name',
                'description',
                'rating',
                'active'
            )
        }
        ),

        ('Prices', {
            'fields': (
                'price',
                'discount_price',
                'on_sale',
            )
        }
        ),
    )

    add_fieldsets = (
        (None,
            {
                'fields': (
                    'ID',
                    'stock_count',
                    'name',
                    'description',
                    'rating',
                    'price',
                    'discount_price',

                )
            },
         ),
    )

    list_display = ('id', 'stock_count', 'name',  'price',
                    'discount_price', 'rating', 'slug')

    list_filter = ('active',   'on_sale',  'rating')

    list_editable = ('stock_count',
                     'price',  'discount_price')

    search_fields = ('name',)

    prepopulated_fields = {"slug": ("name",)}

    # slug is an important field for our site, it is used in
    # all the product URLs. We want to limit the ability to
    # change this only to the owners of the company.

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug"] + ["rating"]

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


# visualize cartline in admin
class CartLineInline(admin.TabularInline):
    model = models.CartLine
    raw_id_fields = ('product', )


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status',)
    list_editable = ('status', )
    list_filter = ('status', )
    inlines = (CartLineInline, )


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductImage, ProductImageAdmin)
admin.site.register(models.Cart, CartAdmin)
