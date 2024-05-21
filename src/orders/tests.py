import datetime

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import UserModel
from orders.models import Order
from stores.models import Store
from products.models import Product


class OrderViewsRenderingTest(TestCase):
    # databases = {"default"}

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="Test user", password="12345")

    def test_orders_list_view(self):
        
        url = reverse("orders:order_list")

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_orders_create_view(self):
        url = reverse("sales:sale_create")

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_orders_update_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        order = Order.objects.create(
            product=product,
            quantity=1,
            order_date=datetime.datetime.now()
        )
        url = reverse("orders:order_update", kwargs={"pk": order.pk})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_orders_delete_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        order = Order.objects.create(
            product=product,
            quantity=1,
            order_date=datetime.datetime.now()
        )
        
        url = reverse("orders:order_delete", kwargs={"pk": order.pk})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        order.status = "2"
        order.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_orders_details_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        order = Order.objects.create(
            product=product,
            quantity=1,
            order_date=datetime.datetime.now()

        )
        url = reverse("orders:order_details", kwargs={"pk": order.pk})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)




