# Generated by Django 4.0.4 on 2022-08-15 14:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='product',
            name='ratings',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MaxValueValidator(5.0, 'Ratings must be between 1 and 5.')], verbose_name='ratings'),
        ),
    ]