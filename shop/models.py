from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import logging
from accounts.models import Address, TITLE_CHOICES, COUNTIES, CITIES, COUNTRIES

from customauth.models import CustomUser
from django.core import exceptions 

logger = logging.getLogger(__name__)


# MODEL MANAGERS
class ActiveManager(models.Manager):
    def active(self):
        '''returns True if product is active'''
        return self.filter(active=True)


class ProductTagManager(models.Manager):
    '''allows working with natural keys to loaddata'''

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

# MODELS


class ProductTag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField('tag_thumbnail')

    objects = ProductTagManager()

    def __str__(self):
        '''returns a string name of each tag'''
        return self.name.title()

    def natural_key(self):
        '''slug used as natural key since it is unlikely to change'''
        return self.slug


class Product(models.Model):

    objects = ActiveManager()

    name = models.CharField(max_length=32)
    tags = models.ManyToManyField(ProductTag, default="all")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    discount_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, default=0.00)
    # ratings = models.DecimalField('ratings', max_digits=4, decimal_places=2, default=0.00, validators=[
    #                               MaxValueValidator(5.00, 'Ratings must be between 1 and 5.')])
    count = models.IntegerField(blank=False, default=1)
    slug = models.SlugField(max_length=48, unique=True, blank=False)
    active = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.title()

    def natural_key(self):
        return self.pk

    @property
    def is_in_stock(self):
        '''returns true if product in stock'''
        return self.count > 0


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

    count = models.PositiveIntegerField('number of items in cart', default=0)

    def is_empty(self):
        return self.cartline_set.all().count() == 0

    def totalPrice(self):
        pass

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

    def price(self):
        '''return the price of each product in cart'''
        return self.product.price * self.quantity


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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=10)

    # , we copy the content of the Address model.
    # This will make orders snapshots in time and
    # any subsequent change to a user’s addresses will not affect existing orders.

    billing_title = models.CharField(max_length=3,  choices=TITLE_CHOICES)
    billing_name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=150)
    billing_postal_code = models.CharField(max_length=12)
    billing_town = models.CharField(max_length=60)
    billing_county = models.CharField(max_length=3, choices=COUNTIES)
    billing_city = models.CharField(max_length=60, choices=CITIES)
    billing_country = models.CharField(max_length=3, choices=COUNTRIES)
    billing_phone_no = models.IntegerField()

    shipping_title = models.CharField(max_length=3,  choices=TITLE_CHOICES)
    shipping_name = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=150)
    shipping_postal_code = models.CharField(max_length=12)
    shipping_town = models.CharField(max_length=60)
    shipping_county = models.CharField(max_length=3, choices=COUNTIES)
    shipping_city = models.CharField(max_length=60, choices=CITIES)
    shipping_country = models.CharField(max_length=3, choices=COUNTRIES)
    shipping_phone_no = models.IntegerField()

    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    last_spoken_to = models.ForeignKey(
        CustomUser,
        null=True,
        related_name="chats",
        on_delete=models.SET_NULL,
    )

    def amount(self):
        '''returns the total order amount'''
        pass


# Customer service will mark orders as PAID,
# and dispatch managers will mark lines with the relevant status


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
