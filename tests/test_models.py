from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from accounts.models import Address
from customauth.models import CustomUser
from django.contrib.auth.models import Group
from shop.models import Product
from django.utils.text import slugify
from shop.models import Cart, CartLine


class TestAuthModel(TestCase):
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

    def testCreateOrderWorks(self):
        fake_user = Faker()

        password = 'Qwerty_Keyboard!'

        p1 = Product.objects.create(
            name='product Three',
            slug=slugify('product-three'),
            price=Decimal('3130.00'),
        )

        p2 = Product.objects.create(
            name='product Four',
            slug=slugify('product-four'),
            price=Decimal('3130.00'),
        )

        user = CustomUser.objects.create_user(
            first_name=fake_user.first_name(),
            last_name=fake_user.last_name(),
            email=fake_user.email(),
            password=password,
        )

        billing = Address.objects.create(
            user=user,
            title='MR.',
            name="John Kimball",
            address="127 Kilimani",
            town='Nairobi',
            city="Nairobi",
            county='047',
            country="KE",

        )

        shipping = billing  # shipping address same as billing address

        cart = Cart.objects.create(user=user)

        CartLine.objects.create(
            cart=cart, product=p1
        )

        CartLine.objects.create(
            cart=cart, product=p2
        )

        with self.assertLogs("shop.models", level="INFO") as logs:
            order = cart.createOrder(billing, shipping)

        # assert generation of logs
        self.assertGreaterEqual(len(logs.output), 1)

        order.refresh_from_db()

        self.assertEquals(order.user, user)

        self.assertEquals(order.billing_address, "127 Kilimani")

        self.assertEquals(order.shipping_address, "127 Kilimani")

        #  more checks to be added
        self.assertEquals(order.lines.all().count(), 2)

        lines = order.lines.all()

        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)


class TestAddressModel(TestCase):
    def test_address_list_page_returns_only_owned(self):
        user1 = CustomUser.objects.create_user(
            first_name='user',
            last_name='1',
            email='user1@domain.ext',
            password='seMePassW@R_d',
            is_active=True,

        )

        user2 = CustomUser.objects.create_user(
            first_name='user',
            last_name='2',
            email='user2@domain.ext',
            password='seMePassW@R_d',
            is_active=True

        )

        Address.objects.create(
            user=user1,
            title='Mr.',
            name='User One',
            address='Address One Goes Here',
            postal_code='10030',
            town='Nairobi',
            county='Nairobi',
            city='Nairobi',
            country='Kenya'
        )

        Address.objects.create(
            user=user2,
            title='Mr.',
            name='User Two',
            address='Address Two Goes Here',
            postal_code='20030',
            town='Nairobi',
            county='Nairobi',
            city='Nairobi',
            country='Kenya'

        )

        self.client.force_login(user2)

        response = self.client.get(reverse("address-list"))

        self.assertEqual(response.status_code, 200)

        address_list = Address.objects.filter(user=user2)
        self.assertEqual(
            list(response.context["object_list"]),
            list(address_list),
        )

    def test_address_create_stores_user(self):
        user3 = CustomUser.objects.create_user(
            first_name='user',
            last_name='3',
            email='user3@domain.ext',
            password='seMePassW@R_d',
            is_active=True,

        )

        post_data = {
            'user': user3,
            'title':  'Mr.',
            'name': 'User Two',
            'address': 'Address Two Goes Here',
            'postal_code': '20030',
            'town': 'Nairobi',
            'county': 'Nairobi',
            'city': 'Nairobi',
            'country': 'Kenya'
        }

        self.client.force_login(user3)
        self.client.post(
            reverse("create-address"), post_data
        )

        self.assertTrue(
            Address.objects.filter(user=user3).exists()
        )
