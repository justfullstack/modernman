from decimal import Decimal
from django.test import TestCase
from faker import Faker
from customauth.models import CustomUser
from django.contrib.auth.models import Group
from shop.models import Product
from django.utils.text import slugify
from shop.models import Cart, CartLine


class TestModel(TestCase):
    def testCustomUserModel(self):
        user = CustomUser.objects.create_user(
            first_name="First",
            last_name="Last",
            email="user1@gmail.com",
            password="my_pAssword!",
            is_subscribed=True
        )

        superuser = CustomUser.objects.create_superuser(
            email="superuser@gmail.com",
            password="my_pAssword!"
        )

        self.assertEqual(len(CustomUser.objects.all()), 2)

        self.assertIsInstance(user, CustomUser)
        self.assertIsInstance(superuser, CustomUser)

        self.assertFalse(user.is_active)

        CustomUser.objects.filter(email=user.email).update(is_active=True)
        user.refresh_from_db()

        self.assertTrue(user.is_active)

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_subscribed)
        self.assertFalse(user.is_employee)
        self.assertFalse(user.is_dispatcher)

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        CustomUser.objects.filter(email=superuser.email).update(is_active=True)
        superuser.refresh_from_db()

        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_employee)
        self.assertTrue(superuser.is_admin)

        CustomUser.objects.filter(email=user.email).update(is_subscribed=True)
        user.refresh_from_db()

        self.assertTrue(user.is_subscribed)


class TestShopModel(TestCase):
    def testProductActiveManagerWorks(self):
        Product.objects.create(
            name='product One',
            slug=slugify('Product One'),
            price=Decimal('3130.00'),
            active=False
        )

        Product.objects.create(
            name='Product Two',
            price=Decimal('3130.00'),
            slug=slugify('Product Two'),
            active=True
        )

        Product.objects.create(
            name='Product Three',
            price=Decimal('170.00'),
            slug=slugify('Product Three'),
            active=True
        )

        self.assertEqual(Product.objects.active().count(), 2)

    def testProductCart(self):

        user = Faker()

        first_name = user.first_name()
        last_name = user.last_name()
        email = user.email()
        password = 'Qwerty_Keyboard!'

        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        product = Product.objects.create(
            name='Product Name',
            price=100,
            slug='product-name'
        )

        cart1 = Cart.objects.create()

        self.assertTrue(cart1.user == None)
        self.assertTrue(cart1.status == 10)

        CartLine.objects.create(cart=cart1, product=product, quantity=3)

        self.assertEqual(cart1.count(), 1)

        cart2 = Cart.objects.create(user=user)

        CartLine.objects.create(cart=cart2, product=product, quantity=3)

        self.assertTrue(cart2.user == user)
        self.assertEqual(cart2.count(), 1)
