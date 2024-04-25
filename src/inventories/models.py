from django.db import models

from products.models import Product
from sales.models import Sale
from orders.models import Order
from stores.models import Store


class Inventory:

    @property
    def products_count(self):
        return Product.objects.all().count()

    @property
    def sales_count(self):
        return Sale.objects.all().count()
    
    @property
    def orders_count(self):
        return Order.objects.all().count()
    
    @property
    def total_earned(self):
        total = 0
        sales = Sale.objects.all()
        for sale in sales:
            total += sale.total_amount
        return total
    
    

