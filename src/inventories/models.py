import decimal
import datetime

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

    default_date_range = None
    default_month = datetime.datetime.now().month
    default_year = datetime.datetime.now().year

    @classmethod
    def products_count(cls, store: Store):
        return Product.objects.filter(store=store).count()
    
    @classmethod
    def get_total_stock(cls, store: Store):
        total = 0
        products = Product.objects.filter(store=store)
        for p in products:
            total += p.stock_quantity
        return total

    @classmethod
    def sales_count(cls, store: Store, month=None, year=None):
        if not year:
            year = cls.default_year
        if not month:
            month = cls.default_month

        return Sale.objects.filter(store=store, 
                                sale_date__year=year,
                                sale_date__month=month).count()
    
    @classmethod
    def orders_count(cls, store: Store, month=None, year=None):
        if not year:
            year = cls.default_year
        if not month:
            month = cls.default_month
        return Order.objects.filter(store=store,
                                order_date__year=year,
                                order_date__month=month).count()

    @classmethod
    def total_earned(cls, store: Store, month=None, year=None):
        if not year:
            year = cls.default_year
        if not month:
            month = cls.default_month
        total =  decimal.Decimal(0.0)
        sales = Sale.objects.filter(store=store, sale_date__year=year, sale_date__month=month)
        for sale in sales:
            total += sale.total_amount

        total_str = format_number_with_space_separator(total)
        # print(total_str)
        return total_str
    
    @classmethod
    def best_products(cls, store: Store, month=None, year=None):
        def func(p):
            return p.get_sales_count(month=month, year=year) > 0

        best_products = []
        products = Product.objects.filter(store=store)
        # best_products = products.filter(lambda p: p.get_sales_count(month=month, year=year) > 0)
        best_products = list(filter(func, list(products)))
        best_products = sorted(products, key=lambda p: p.get_sales_count(month=month, year=year), reverse=True)
        return best_products[:5]

    @classmethod
    def out_of_stock_products(cls, store: Store):
        return Product.objects.all().filter(store=store).filter(stock_quantity__lte=10)[:7]