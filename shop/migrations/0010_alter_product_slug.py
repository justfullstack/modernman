# Generated by Django 5.0.6 on 2024-06-07 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_billing_address_order_billing_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=48, null=True),
        ),
    ]
