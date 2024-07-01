import decimal
import datetime

from django.db import models

from sales.models import Sale, SaleStatus
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
    def get_recent_sales(cls, store: Store, from_date: datetime.date, to_date: datetime.date, limit: int=10):
        return store.sale_set.filter(status=SaleStatus.VALIDATED, add_at__range=[from_date, to_date]).order_by("-sale_date")[:limit]

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
    def sales_count(cls, store: Store, from_date: datetime.date, to_date: datetime.date):
        return Sale.objects.filter(store=store, status=SaleStatus.VALIDATED,
                                add_at__range=[from_date, to_date]).count()
    
    @classmethod
    def orders_count(cls, store: Store, from_date: datetime.date, to_date: datetime.date):
        return Order.objects.filter(store=store, add_at__range=[from_date, to_date]).count()

    @classmethod
    def total_earned(cls, store: Store, from_date: datetime.datetime, to_date: datetime.datetime):
        total =  decimal.Decimal(0.0)
        sales = Sale.objects.filter(store=store, status=SaleStatus.VALIDATED, add_at__range=[from_date, to_date])
        for sale in sales:
            total += sale.total_amount

        total_str = format_number_with_space_separator(total)
        # print(total_str)
        return total_str
    
    @classmethod
    def net_incomme(cls, store: Store, from_date: datetime.date, to_date: datetime.date):
        total =  decimal.Decimal(0.0)
        sales = Sale.objects.filter(store=store, status=SaleStatus.VALIDATED, add_at__range=[from_date, to_date])
        for sale in sales:
            total += sale.income
        total -= cls.get_shipping_fees(store=store, from_date=from_date, to_date=to_date, string=False)
        total_str = format_number_with_space_separator(total)
        return total_str

    @classmethod
    def best_seller_products(cls, store: Store, from_date: datetime.date, to_date: datetime.date):
        best_products = []
        products = Product.objects.filter(store=store)
        for product in products:
            p = (product, product.get_sales_count(from_date=from_date, to_date=to_date))
            if p[1] and p[1] > 0:
                best_products.append(p)
        best_products.sort(key=lambda x: x[1], reverse=True)
        return best_products[:5]

    @classmethod
    def out_of_stock_products(cls, store: Store):
        return Product.objects.all().filter(store=store).filter(stock_quantity__lte=10)\
                .order_by("stock_quantity")[:7]
    
    @classmethod
    def get_shipping_fees(cls, store: Store, from_date: datetime.date, to_date: datetime.date, string=False):
        total_fees = decimal.Decimal(0.0)
        orders = Order.objects.filter(store=store, add_at__range=[from_date, to_date])
        for order in orders:
            if order.shipping_costs:
                total_fees += order.shipping_costs
        if string:
            total_fees = format_number_with_space_separator(total_fees)
        return total_fees




