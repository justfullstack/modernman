import logging
from django.db.models.signals import pre_save, post_save
from .models import Order, OrderLine, ProductImage, Cart
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderLine)
def moveFromOrderLineToOrderStatus(sender, instance, **kwargs):
    """ 
    signal will be executed after saving instances of the OrderLine model. It completes order: making sure that the marked orders do not appear in the list api anymore.
    """

    # check whether any order lines connected to the
    # order have statuses below “sent.” If there is
    # terminate  execution, else mark the
    # whole order as done
    if not instance.order.lines.filter(status__lt=OrderLine.SENT).exists():
        logger.info(
            f'All lines for order {instance.order.id} procesed. Marking as done...')
        instance.order.status = Order.DONE
        instance.order.save()


# Merge cart on login (session change)
@receiver(user_logged_in)
def mergeCartsOnLogin(sender, user, request, **kwargs):
    '''merges carts belonging to a user on session change'''

    anonymous_cart = getattr(request, "cart", None)

    if anonymous_cart:
        try:
            # get authenticated 'OPEN' cart
            loggedin_cart = Cart.objects.get(
                user=user,
                status=Cart.OPEN
            )

            # merge with anonymous cart
            for line in anonymous_cart.cartline_set.all():
                line.cart = loggedin_cart
                line.save()

            # dump anonymous cart
            anonymous_cart.delete()

            request.cart = loggedin_cart

            logger.info(f"Merged cart to id {loggedin_cart.id}")

        except Cart.DoesNotExist:
            # if no cart to merge
            anonymous_cart.user = user
            anonymous_cart.save()
            logger.info(f"Assigned user to cart id {anonymous_cart.id}")
