from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from customauth.forms import UserCreationForm, AuthenticationForm
from customauth.models import CustomUser
from shop.models import Cart, CartLine, Product
from django.utils.text import slugify


class AuthenticationView(TestCase):
    def testUserSignupPageLoadsCorrectly(self):

        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/signup.html")
        self.assertContains(response, "Join ModernMan")
        self.assertIsInstance(response.context["form"], UserCreationForm)

    def testUserSignupPageSubmissionWorks(self):
        post_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "user1@gmail.com",
            "password1": "my_pAssword!",
            "password2": "my_pAssword!",
        }

        with patch.object(UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(
                reverse("signup"),
                post_data
            )

        # confirm redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            email=post_data["email"]).exists())
        mock_send.assert_called_once()

    def testUserAuthenticationPageLoadsCorrectly(self):

        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertContains(response, "Welcome Back")
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def checkUserAuthenticationWorks(self):
        user = CustomUser.objects.create_user(
            first_name="First",
            last_name="Last",
            email="user1@gmail.com",
            password="my_pAssword!",
            is_subscribed=True
        )

        user.save()

        login_post_data = {
            "email": user.email,
            "password": user.password,
        }

        response = self.client.post(reverse("login"), login_post_data)

        # confirm redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            email=user.email).exists())

        self.assertTrue(auth.get_user(self.client).is_authenticated)


class TestShopView(TestCase):
    def testProductDetailPageLoadCorrectly(self):

        product = Product.objects.create(
            name='Product One Test',
            slug='product-one-test',
            price=3452,
            ratings=5

        )

        product.save()

        response = self.client.get(
            reverse("product", kwargs={'slug': product.slug}))

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(
        #    response, "  shop/product_detail.html", count=1)
        self.assertContains(response, product.name)

    def testAddToCartLoggedInWorks(self):
        user = CustomUser.objects.create_user(
            first_name='First',
            last_name='Last',
            email='email@domain.ext',
            password='Qwerty_keyboardr!',
        )

        product = Product.objects.create(
            name='product One',
            slug=slugify('Product One'),
            price=Decimal('3130.00')
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("add-to-cart"), {"product_id": product.id}
        )

        self.assertTrue(
            response.status == 200
        )

        self.assertTrue(
            Cart.objects.filter(user=user).exists()
        )

        self.assertEquals(CartLine.objects.filter(cart__user=user).count(),  1)

        response = self.client.get(
            reverse("add-to-cart"), {"product_id": product.id}
        )

        self.assertTrue(
            response.status == 200
        )

        self.assertEquals(CartLine.objects.filter(cart__user=user).count(), 2)
