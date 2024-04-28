import decimal

from django.db import models

from sales.models import Sale
from orders.models import Order
from stores.models import Store
from products.models import Product


def format_number_with_space_separator(number):
    try:
        total_str, after_comma = str(number).split(".")[0], str(number).split(".")[1]
    except IndexError:
        total_str = str(number)
        after_comma = "00"

    formatted_number = ""
    c = 0
    for i in range(1, len(total_str)+1):
        formatted_number = total_str[-i] + formatted_number 
        c += 1
        if c == 3:
            formatted_number = " " + formatted_number
            c = 0
    formatted_number = formatted_number + "." + after_comma
    return formatted_number 


class Inventory:

    @classmethod
    def products_count(cls, store: Store):
        return Product.objects.filter(store=store).count()

    @classmethod
    def sales_count(cls, store: Store):
        return Sale.objects.filter(store=store).count()
    
    @classmethod
    def orders_count(cls, store: Store):
        return Order.objects.filter(store=store).count()

    @classmethod
    def total_earned(cls, store: Store):
        total =  decimal.Decimal(0.0)
        sales = Sale.objects.filter(store=store)
        for sale in sales:
            total += sale.total_amount

        total_str = format_number_with_space_separator(total)
        # print(total_str)
        return total_str
    
    @classmethod
    def best_products(cls, store: Store):
        products = [p for p in Product.objects.filter(store=store)] 
        best_products = sorted(products, key=lambda p: p.sale_set.all().count(), reverse=True)
        best_products = filter(lambda p: p.sale_set.all().count() > 0, best_products)
        return list(best_products) 

    @classmethod
    def out_of_stock_products(cls, store: Store):
        return Product.objects.all().filter(store=store).filter(stock_quantity__lte=10)