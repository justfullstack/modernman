
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from customauth.models import CustomUser
from shop.models import Cart, CartLine, Product, ProductImage
from django.core.files.images import ImageFile


class Tesignal(TestCase):
    def testCartMergeSignalWorks(self):
        user = CustomUser.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@domain.com",
            password="Password!"
        )

        product1 = Product.objects.create(
            name="Sample Product One",
            slug='product-1',
            price=Decimal('78.50')
        )

        product2 = Product.objects.create(
            name="Sample Product Two",
            slug='product-2',
            price=Decimal('100.00')
        )

        # add anonymous  cart
        response = self.client.get(
            reverse('addToCart'),
            {'product_slug': product1.slug}
        )

        # add to  anonymous cart
        anonymous_cart = Cart.objects.create(user=user)

        # add to cartline
        CartLine.objects.create(
            cart=anonymous_cart,
            product=product2,
            quantity=2
        )

        CartLine.objects.create(
            cart=anonymous_cart,
            product=product1, 
        )

        # log in: should trigger merge signal
        response = self.client.post(
            reverse('login'),
            {'email': "email@domain.com", "password": "Password!"}
        )

        # confirm login
        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )
        # verify cart contents
        self.assertTrue(Cart.objects.filter(user=user).exists())

        cart = Cart.objects.get(user=user)

        self.assertEqual(cart.count(), 3)

    def testThumbnailsGenerationSignal(self):
        # create product
        product3 = Product.objects.create(
            name="Sample Product Two",
            slug='product-3',
            price=Decimal('100.00')
        )

        product3.save()

        # add product image
        with open("modernman/core/fixtures/img/product1.png", "rb") as file:

            image = ProductImage(
                product=product3,
                image=ImageFile(file, name="product1.png")
            )

        # ensure logs generated on success save
        with self.assertLogs("shop", level="INFO") as cm:
            image.save()
            self.assertGreaterEqual(len(cm.output), 1)
            image.refresh_from_db()

        with open("modernman/fixtures/img/product1.png", "rb") as file:
            expected_content = file.read()
            self.assertEquals(image.thumbnail.read(), expected_content)

            # db flushed automatically but not files
            # so flush images manually
            image.thumbnail.delete(save=False)
            image.image.delete(save=False)
