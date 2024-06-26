from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Group


class CustomUserManager(BaseUserManager):
    """A custom manager for our custom authentication model"""

    use_in_migrations = True

    def create_user(self, first_name, last_name, email, password=None, is_subscribed=False):

        if not (first_name and last_name):
            raise ValueError(_("Both names are required!"))

        if not email:
            raise ValueError(_("Email address is required!"))

        try:
            validate_email(email)

        except ValidationError:
            raise ValueError(_("Invalid email address!"))

        email = self.normalize_email(email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        if is_subscribed:
            user.is_subscribed = True

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email address is required!"))
        # validate email
        try:
            validate_email(email)

        except ValidationError:
            raise ValueError(_("Invalid email address!"))

        if not password:
            raise ValueError(_("Password is required!"))

        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        superuser = self.model(email=self.normalize_email(email))
        superuser.set_password(password)

        # set permissions
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.is_admin = True

        if not superuser.is_superuser:
            raise ValueError(_("Superuser must have is_superuser=True."))

        if not superuser.is_staff:
            raise ValueError(_("Superuser must have is_staff=True."))

        superuser.save(using=self._db)

        return superuser


class CustomUser(AbstractBaseUser):

    objects = CustomUserManager()

    username = None
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    first_name = models.TextField(
        'first_name',
        max_length=30,
        null=True,
        blank=True
    )

    last_name = models.TextField(
        'last_name',
        max_length=30,
        null=True,
        blank=True
    )

    email = models.EmailField(
        'email address',
        max_length=200,
        unique=True
    )

    password = models.TextField(
        'password',
        max_length=150,
        null=True,
        blank=True
    )

    avatar = models.ImageField(null=True, blank=True, default="media/avatars/default-avatar.png")

    date_joined = models.DateTimeField(
        'date_joined',
        null=True,
        blank=True,
        auto_now_add=True
    )

    last_login = models.DateTimeField(
        'last_login',
        null=True,
        blank=True
    )

    is_subscribed = models.BooleanField(
        'is_subscribed',
        default=False,
        blank=True
    )

    is_active = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_superuser = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_admin = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_employee = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_dispatcher = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    groups = models.ManyToManyField(Group,  blank=True)

    def __str__(self):
        return f'{self.email}({self.first_name} {self.last_name})'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app ‘app_label‘?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        self.is_staff = self.is_admin

        self.is_employee = self.is_active and (
            self.is_superuser
            or self.is_staff
            or self.groups.filter(name='Employees').exists()
        )

        self.is_dispatcher = self.is_active and (
            self.is_superuser
            or self.is_staff
            and self.groups.filter(name="Dispatchers").exists()
        )
        super().save(*args, **kwargs)



 