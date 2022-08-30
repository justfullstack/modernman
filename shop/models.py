from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import logging
from accounts.models import Address, TITLE_CHOICES, COUNTIES, CITIES, COUNTRIES
from django.urls import reverse
from customauth.models import CustomUser
from django.core import exceptions 

logger = logging.getLogger(__name__)


# MODEL MANAGERS
class ActiveManager(models.Manager):
    def active(self):
        '''returns True if product is active'''
        return self.filter(active=True)

 


# MODELS

class Product(models.Model):

    objects = ActiveManager()


    TAGS = [
        ('Suits', 'Suits'),
        ('Shoes', 'Shoes'),
        ('Blazers', 'Blazers'),
        ('Sweaters', 'Sweaters'),
        ('Accessories', 'Accessories'),
        ('Jewellery', 'Jewellery'),
        ('Perfumes', 'Perfumes'),
        ('Shirts', 'Shirts'),
        ('Trousers', 'Trousers'),
        ('Jackets', 'Jackets'),
        ('Caps', 'Caps'),
        ('Shorts', 'Shorts'),
        ]

    name = models.CharField(max_length=32)
    category = models.TextField(choices=TAGS, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, default=0.00)
    # ratings = models.DecimalField('ratings', max_digits=4, decimal_places=2, default=0.00, validators=[
    #                               MaxValueValidator(5.00, 'Ratings must be between 1 and 5.')])
    stock_count = models.IntegerField(blank=False, default=1)
    slug = models.SlugField(max_length=48, unique=True, blank=False)
    active = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.title()
 
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})


    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})
 

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")
    thumbnail = models.ImageField(upload_to="product_thumbnails", null=True)

 


class Order(models.Model):
    """ 
    While CartLine can contain a number of products, OrderLine will have exactly one entry per product ordered. The reason for this is that we want a status field to have the granularity of a single ordered item.

    Customer service will mark orders as PAID, and dispatch managers will mark lines with the relevant status
    """

    # order statuses
    NEW = 10
    PAID = 20
    DONE = 30

    STATUSES = (
        ('NEW', 'New'),
        ('PAID', 'Paid'),
        ('DONE', 'Done')
    )


    status = models.IntegerField(choices=STATUSES, default=10)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None) 
 


 
class OrderLine(models.Model):
    NEW = 10
    PROCESSING = 20
    SENT = 30
    CANCELLED = 40

    STATUSES = (
        ('NEW', 'New'),
        ('PROCESSING', 'Processing'),
        ('SENT', 'Sent'),
        ('CANCELLED', 'Cancelled')
    )

    # related name allows access via  order.lines.all() instead of the default order.orderline_set.all()
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_lines")
    # impeding deletion of any products that are in an order
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUSES, default=NEW)


class Cart(models.Model):
    """a cart for a user=user or user=None if not authenticated"""

    OPEN = 10
    SUBMITTED = 20

    STATUSES = [
        (OPEN, "Open"),
        (SUBMITTED, "Submitted")
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    status = models.IntegerField(
        choices=STATUSES,
        default=OPEN
    )


    def is_empty(self):
        return self.cartline_set.all().count() == 0

 
    def createOrder(self, billing_address, shipping_address):
        '''creates an order from the cotents of the cart'''
        if not self.user:
            raise exceptions.CartException('Cannot create order withouta user')

        logger.info(
            f'Creating order for cart {self.id} , shipping_address_id={shipping_address.id}, billing_address_id={billing_address.id}')

        order_data = {
            "user": self.user,
            "billing_title": billing_address.title,
            "billing_name": billing_address.name,
            "billing_address": billing_address.address,
            "billing_postal_code": billing_address.postal_code,
            "billing_town": billing_address.town,
            "billing_county": billing_address.county,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "billing_phone_no": billing_address.phone_no,
            "shipping_title": shipping_address.title,
            "shipping_name": shipping_address.name,
            "shipping_address": shipping_address.address,
            "shipping_postal_code": shipping_address.postal_code,
            "shipping_town": shipping_address.town,
            "shipping_county": shipping_address.county,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
            "shipping_phone_no": shipping_address.phone_no,
        }

        order = Order.objects.create(**order_data)

        lines_count = 0

        for line in self.cartline_set.all():
            for item in range(line.quantity):  # **

                order_line_data = {
                    "order": order,
                    "product": line.product
                }

                OrderLine.objects.create(**order_line_data)
                lines_count += 1

        logger.info(
            f'created order with id {order.id} and lines_count {lines_count}')

        # update current cart's status to submitted
        self.status = Cart.SUBMITTED
        self.save()
        return order


class CartLine(models.Model):
    '''links back to the Cart'''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])






