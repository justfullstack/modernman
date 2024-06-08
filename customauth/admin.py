import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from customauth.models import CustomUser
from django.contrib.auth.models import Group

import logging

logger = logging.getLogger(__name__)


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            )
        }
        ),

        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
            )
        }
        ),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_superuser',
                'groups',
            )
        }
        ),

        ('Important Dates', {
            'fields': (
                'last_login',
            )
        }
        ),


    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None,
         {'classes': ('wide',),
          'fields': (
             'email',
             'password1',
             'password2'
         )
         },
         ),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        'is_active',
        'is_admin'
    )

    list_filter = ('is_active', 'is_admin', )

    search_fields = (
        "email",
        "first_name",
        "last_name"
    )

    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin) 