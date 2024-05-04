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
    def net_incomme(cls, store: Store, month=None, year=None):
        if not year:
            year = cls.default_year
        if not month:
            month = cls.default_month
        total =  decimal.Decimal(0.0)
        sales = Sale.objects.filter(store=store, sale_date__year=year, sale_date__month=month)
        for sale in sales:
            total += sale.income

        total_str = format_number_with_space_separator(total)
        return total_str

    @classmethod
    def best_products(cls, store: Store, month=None, year=None):
        month = cls.default_month if not month else month
        year = cls.default_year if not year else year

        best_products = []
        products = Product.objects.filter(store=store)
        for product in products:
            p = (product.name, product.get_sales_count(month=month, year=year))
            if p[1] and p[1] > 0:
                best_products.append(p)
        best_products.sort(key=lambda x: x[1], reverse=True)
        return best_products[:5]

    @classmethod
    def out_of_stock_products(cls, store: Store):
        return Product.objects.all().filter(store=store).filter(stock_quantity__lte=10)\
                .order_by("stock_quantity")[:7]
    
    @classmethod
    def get_shipping_fees(cls, store: Store, month=None, year=None):
        if not year:
            year = cls.default_year
        if not month:
            month = cls.default_month

        total_fees = decimal.Decimal(0.0)
        orders = Order.objects.filter(store=store, order_date__month=month, order_date__year=year)
        for order in orders:
            if order.shipping_costs:
                total_fees += order.shipping_costs
        return total_fees




