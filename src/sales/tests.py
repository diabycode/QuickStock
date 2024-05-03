import datetime

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import login
from django.urls import reverse

from accounts.models import UserModel
from sales.models import Sale
from stores.models import Store
from products.models import Product


class SaleViewsRenderingTest(TestCase):
    databases = {"default"}

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="Test user", password="12345")
    
    def test_sales_list_view(self):
        
        url = reverse("sales:sale_list")

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

    def test_sales_create_view(self):
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

    def test_sales_details_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        sale = Sale.objects.create(
            sale_date=str(datetime.datetime.now().date()),
            product=product
        )
        url = reverse("sales:sale_update", kwargs={"pk": sale.pk})

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

    def test_sales_update_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        sale = Sale.objects.create(
            sale_date=str(datetime.datetime.now().date()),
            product=product
        )
        url = reverse("sales:sale_update", kwargs={"pk": sale.pk})

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

    def test_sales_delete_view(self):
        product = Product.objects.create(name="Product test")
        product.stock_quantity += 2
        product.save()
        sale = Sale.objects.create(
            sale_date=str(datetime.datetime.now().date()),
            product=product
        )
        url = reverse("sales:sale_delete", kwargs={"pk": sale.pk})

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
        sale.status = "2"
        sale.save()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)









