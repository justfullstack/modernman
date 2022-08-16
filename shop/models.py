from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import logging

from sympy import product
from customauth.models import CustomUser


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
    ratings = models.DecimalField('ratings', max_digits=4, decimal_places=2, default=0.00, validators=[
                                  MaxValueValidator(5.00, 'Ratings must be between 1 and 5.')])
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

    def is_empty(self):
        return self.cartline_set.all().count() == 0

    def count(self):
        return self.cartline_set.all().count()

    def totalPrice(self):
        pass


class CartLine(models.Model):
    '''links back to the Cart'''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])

    def price(self):
        '''return the price of each product in cart'''
        return self.product.price * self.quantity
