# Generated by Django 4.0.4 on 2022-08-30 21:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_order_items_delete_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartline',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]