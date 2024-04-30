from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from orders.signals import order_shipped_signal, order_cancelled_signal
from sales.models import Sale
from sales.signals import sale_cancelled_signal
from orders.models import Order, OrderStatus


@receiver(post_save, sender=Sale)
def update_quantity_on_sale_confirmation(sender, instance, created, **kwargs):

    if created:
        product = instance.product

        # Update quantity
        product.stock_quantity -= instance.quantity
        product.save()

        # print(f"Quantity updated for {product.name}. New quantity: {product.stock_quantity}")

@receiver(sale_cancelled_signal)
def update_quantity_on_sale_cancellation(sender, instance, **kwargs):
    
    product = instance.product

    # Update quantity
    product.stock_quantity += instance.quantity
    product.save()

    # print(f"Quantity updated for {product.name}. New quantity: {product.stock_quantity}")

@receiver(order_shipped_signal)
@receiver(post_save, sender=Order)
def update_quantity_on_order_shipped(sender, instance, **kwargs):
    # update de shipped product quantity
    if instance.status == OrderStatus.SHIPPED:
        product = instance.product
        product.stock_quantity += instance.quantity
        product.save()
    
        # print(f"Quantity updated for {product.name}. New quantity: {product.stock_quantity}")

@receiver(order_cancelled_signal)
def update_quantity_on_order_cancelled(sender, instance, **kwarsg):
    
    # update de shipped product quantity
    product = instance.product
    product.stock_quantity -= instance.quantity
    product.save()
    
    # print(f"Quantity updated for {product.name}. New quantity: {product.stock_quantity}")