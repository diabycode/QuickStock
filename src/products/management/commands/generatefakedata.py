from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from products.models import Product
from sales.models import Sale, SaleStatus
from orders.models import Order, OrderStatus
from stores.models import Store


fk = Faker(locale="fr_FR")

PRODUCT_NAMES = [
    "Acier renforcé",
    "Adhésif industriel",
    "Aluminium laminé",
    "Ampoules LED",
    "Appareils de mesure de précision",
    "Attaches de câble en nylon",
    "Batteries industrielles",
    "Câbles électriques blindés",
    "Caisse enregistreuse numérique",
    "Caméras de sécurité IP",
    "Capteurs de température",
    "Cartouches d'encre pour imprimantes",
    "Chariots élévateurs électriques",
    "Climatiseurs industriels",
    "Compresseurs d'air",
    "Conteneurs de stockage",
    "Dispositifs de verrouillage électronique",
    "Échafaudages en aluminium",
    "Écrans de protection anti-éclaboussures",
    "Équipement de protection individuelle (EPI)",
    "Étiqueteuses automatiques",
    "Fournitures de nettoyage industriel",
    "Générateurs diesel",
    "Gilets de sécurité haute visibilité",
    "Grues hydrauliques",
    "Imprimantes multifonctions",
    "Lames de scie circulaire carbure",
    "Lampes de travail à LED",
    "Lève-palettes manuels",
    "Logiciels de gestion des stocks",
    "Machine de fabrication de sacs en plastique",
    "Matériel de levage industriel",
    "Miroirs de sécurité",
    "Outils pneumatiques",
    "Palettes en plastique",
    "Panneaux solaires",
    "Pompes à eau submersibles",
    "Rayonnages industriels",
    "Rubans adhésifs doubles face",
    "Scellants de silicone",
    "Systèmes d'alarme incendie",
    "Tablettes industrielles",
    "Tapis antidérapants",
    "Tours de refroidissement",
    "Transpalettes électriques",
    "Uniformes de travail",
    "Valises de transport résistantes aux chocs",
    "Véhicules utilitaires électriques",
    "Vis de fixation en acier inoxydable",
    "Vitrines réfrigérées"
]

def get_random_person_name():
    return fk.unique.name()

def get_random_num(range_start: int, range_end: int):
    return fk.random_int(range_start, range_end)

def get_random_date(range_start=None, range_end=None):
    return fk.date_between_dates(date_start=range_start, date_end=range_end)


class Command(BaseCommand):
    help = "Generate fake data for demo"

    def add_arguments(self, parser):
        """
        Data for a month :
            --products-count -pc  default=50
            --orders-max   -oc  default=100
            --sales-max    -sc  default=3000
        """

        parser.add_argument("--products-count", "-pc", dest="products_count", type=int, default=50, help="Number of products to gen")
        parser.add_argument("--orders-max", "-oc", dest="orders_max", type=int, default=100, help="Limit of orders to gen")
        parser.add_argument("--sales-max", "-sc", dest="sales_max", type=int, default=3000, help="Limit of sales to gen")

    def handle(self, *args, **options):
        """
        
        loop : products-count 50
            - create product [name, quantity:5, wholesale_unit_price:(7000, 25000),
                                unit_price_sale:whole+2000]

            if orders-max: 
                - generate orders for this product
                    :: orders-max 100
                    - choose arbitrary orders_count [2-15] 
                        if orders_count > orders-max:
                            orders_count = orders-max
                            orders-max = 0
                        else:
                            orders-max -= orders_count

                    - loop : orders_count
                        - create order and assign to product (
                            product: product
                            quantity: [15-50]
                            order_date: [ now+{abitrary-num[1-30]}days ]
                            arrived_date: order_date 
                            shipping_costs: [1500-20000]
                            status: shipped
                            provider_name: to_gen
                        )

            if sales-max:
                - generate sales for this product
                    :: sales-max 3000
                    - choose arbitrary sales_count [2-15]
                        if sales_count > sales-max:
                            sales_count = sales-max
                            sales-max = 0
                        else :
                            sales-max -= sales_count
                    - loop : sales_count

                        Risk : ValueError("Quantity sold can't exceed the stock quantity.")
                        - create sale and assign to product (
                            sale_date: [ now+{abitrary-num[1-30]}days ]
                            product: product
                            quantity: [5-20]
                            buyer_name: to_gen
                        )   

        """
        
        products_count: int = options.get("products_count")
        if products_count > 50:
            raise ValueError("The number of products can't exceed 50")
        orders_max: int = options.get("orders_max")
        sales_max: int = options.get("sales_max")

        stores = [s for s in Store.objects.all()]

        print(f"Generating for {products_count} products...")
        for i in range(products_count):
            # create product [name, quantity:5, wholesale_unit_price:(7000, 25000), 
                                # unit_price_sale:whole+2000]

            store = random.choice(stores)

            product = Product()
            product.name = PRODUCT_NAMES.pop()
            product.stock_quantity = 5
            product.store = store
            product.wholesale_unit_price = get_random_num(7000, 25000)
            product.unit_price_sale = product.wholesale_unit_price + get_random_num(2000, 7000)
            product.save()

            # generate orders for this product
            if orders_max: 
                
                # choose arbitrary orders_count [2-15] 
                orders_count = get_random_num(2, 15)
                if orders_count > orders_max:
                    orders_count = orders_max
                    orders_max = 0
                else:
                    orders_max -= orders_count

                # loop : orders_count
                for i in range(orders_count):
                    # create order and assign to product 
                    order = Order(product=product)
                    order.quantity = get_random_num(15, 50)

                    order_date = get_random_date(
                        datetime.now().date(),
                        datetime.now().date() + timedelta(days=30)
                    )
                    order.order_date = order_date
                    order.arrived_date = order_date 
                    order.store = store
                    order.shipping_costs = get_random_num(1500, 20000)
                    order.status = OrderStatus.SHIPPED
                    order.provider_name = get_random_person_name()
                    order.save()

            # generate sales for this product
            if sales_max:
                # -choose arbitrary sales_count [2-15]
                sales_count = get_random_num(2, 15)
                if sales_count > sales_max:
                    sales_count = sales_max
                    sales_max = 0
                else :
                    sales_max -= sales_count
            
            
                # loop : sales_count
                for i in range(sales_count):
                    sale = Sale(product=product)
                    sale.quantity = get_random_num(5, 20)
                    sale.sale_date = get_random_date(
                        datetime.now().date(),
                        datetime.now().date() + timedelta(days=30),
                    ) 
                    sale.store = store
                    sale.buyer_name = get_random_person_name()
                    
                    # Risk : ValueError("Quantity sold can't exceed the stock quantity.")
                    try:
                        sale.save()
                    except ValueError:
                        print(f"'{product}' has insufficient quantity ({product.stock_quantity})")
                        break
        
            print(f"{product.name.capitalize()}")
