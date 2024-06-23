from django.dispatch import Signal


def order_cancelled_signal_callback(sender, instance, **kwargs):
    if instance.added_to_stock:
        product = instance.product
        product.stock_quantity -= instance.quantity
        if product.stock_quantity < 0:
            raise ValueError("Impossible d'annuler cette commande")
        product.save()

order_cancelled_signal = Signal()
order_cancelled_signal.connect(order_cancelled_signal_callback)


def order_shipped_signal_callback(sender, instance, **kwargs):
    if not instance.added_to_stock and instance.is_shipped:
        product = instance.product
        product.stock_quantity += instance.quantity
        product.save()
        instance.added_to_stock = True
        instance.save()

order_shipped_signal = Signal()
order_shipped_signal.connect(order_shipped_signal_callback)

