from django.db import models
from django.urls import reverse
import logging

from matplotlib.image import thumbnail


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
