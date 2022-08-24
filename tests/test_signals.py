
from decimal import Decimal
from django.urls import reverse
from django.contrib import auth
from customauth.models import CustomUser
from shop.models import Cart, CartLine, Product


def testCartMergeSignalWorks(self):
        user = CustomUser.objects.create_user(
                                first_name="First", 
                                last_name="Last" ,
                                email="email@domain.com", 
                                password="Password!"
                                )
        
        product1 = Product.objects.create(
                                name="Sample Product One",
                                description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Reprehenderit ratione, ut quo consequuntur fugit sapiente dicta deleniti neque dolor temporibus autem a vero, et suscipit id deserunt. Harum, soluta delectus?",
                                price=Decimal('78.50')
                                )

        product2 =  Product.objects.create(
                                name="Sample Product Two",
                                description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Reprehenderit ratione, ut quo consequuntur fugit sapiente dicta deleniti neque dolor temporibus autem a vero, et suscipit id deserunt. Harum, soluta delectus?",
                                price=Decimal('100.00')
                                )

        # add anonymous  cart
        response = self.client.get(
                            reverse('addToCart'),
                            {'product_id': product1.id}   
                            )
                                
        # add to  cart logged_in
        cart1 = Cart.objects.create(user=user)


        # add to cartline
        CartLine.objects.create(
                            cart=cart1,
                            product=product2,
                            quantity=2
                            )

        # log in: should trigger merge signal
        response = self.client.post(
                            reverse('login'),
                            {'email': "email@domain.com", "password": "Password!"}   
                            )



        self.assertTrue(
            auth.get_user(self.client).is_authenticated
            )

        self.assertTrue(Cart.objects.filter(user=user).exists())

        cart =  Cart.objects.get(user=user)  
        self.assertEqual(cart.count(), 3)