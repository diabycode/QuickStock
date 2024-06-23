from django.dispatch import Signal


sale_cancelled_signal = Signal()


def deduct_sale_from_stock_callback(sender, instance, **kwargs):
    for saleproduct in instance.saleproduct_set.all():
        product = saleproduct.product
        if not saleproduct.is_locked and not product.stock_quantity - saleproduct.quantity < 0:
            product.stock_quantity -= saleproduct.quantity
            product.save()
            saleproduct.is_locked = True
            saleproduct.save()

deduct_sale_from_stock = Signal()
deduct_sale_from_stock.connect(deduct_sale_from_stock_callback)


def restore_stock_callback(sender, instance, **kwargs):
    for saleproduct in instance.saleproduct_set.all():
        product = saleproduct.product
        product.stock_quantity += saleproduct.quantity
        product.save()

restore_stock = Signal()
restore_stock.connect(restore_stock_callback)
