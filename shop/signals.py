import logging
from django.db.models.signals import pre_save, post_save
from .models import Order, OrderLine, ProductImage, Cart
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderLine)
def move_from_orderline_to_order_status(sender, instance, **kwargs):
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
