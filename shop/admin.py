import logging
from django.contrib import admin
from django.utils.html import format_html

logger = logging.getLogger(__name__)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count',
                    'on_sale', 'slug',  'price')
    list_filter = ('active',    'on_sale',  'date_uploaded')
    list_editable = ('count',  'price', 'description')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name")}
    autocomplete_fields = ('tags',)

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
    readonly_field = ("description", "price", "tags", "active")
    list_filter = ("active", )
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name", )}


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ("active")
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ()

    # tag slugs also appear in urls, therefore it is a
    # property only owners can change

    def get_readonly_fields(self, request):
        if not request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    def get_prepopulated_fields(self, request, obj):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


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
