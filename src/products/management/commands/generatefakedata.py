from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Generate fake data for demo"

    def add_arguments(self, parser):
        """
        Data for a month :
            --products-count -pc  default=50
            --orders-max   -oc  default=100
            --sales-max    -sc  default=3000
        """

        parser.add_argument("--products-count", "-pc", type=int, default=50, help="Number of products to gen")
        parser.add_argument("--orders-max", "-oc", type=int, default=100, help="Limit of orders to gen")
        parser.add_argument("--sales-max", "-sc", type=int, default=3000, help="Limit of sales to gen")

    def handle(self, *args, **options):
        """
        LOG : generating for {products-count} products...
        loop : products-count 50
            - create product [name, quantity:5, wholesale_unit_price:(7000, 25000),
                                unit_price_sale:whole+2000]
            - generate orders for this product
                :: orders-max 100
                - choose arbitrary orders_count [2-15] and : (orders-max - orders_count)
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
            - generate sales for this product
                :: sales-max 3000
                - choose arbitrary sales_count [2-15] and : (sales-max - sales_count)
                - loop : sales_count
                    - create sale and assign to product (
                        sale_date: [ now+{abitrary-num[1-30]}days ]
                        product: product
                        quantity: [5-20]
                        buyer_name: to_gen
                    )
            LOG : {product-name} :stock {product.stock_q} :orders {orders_count} :sales {sales_count}

        functions/methods
            - get_random_product_name()
            - get_random_person_name()
            - get_random_num(range_start, range_end)
            - get_random_date(range_start, range_end)
        """
        
        pass

