# Generated by Django 4.1.3 on 2022-11-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0004_alter_customuser_avatar_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_joined'),
        ),
    ]
