from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import login
from django.urls import reverse

from accounts.models import UserModel
from products.models import Product
from stores.models import Store


class ProductViewsRenderingTest(TestCase):
    # databases = {"default"}

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="Test user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", email="almamy@gmail.com", password="12345")

    def test_products_list_view(self):
        
        url = reverse("products:product_list")

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        self.assertIn("permission_denied", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_products_create_view(self):

        url = reverse("products:product_create")

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url)
        self.assertIn("permission_denied", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)

        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_products_update_view(self):

        product = Product.objects.create(name="Product test")
        url = reverse("products:product_update", kwargs={"slug": product.slug})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")


        response = self.client.get(url) 
        self.assertIn("permission_denied", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url) 
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk})) 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)

    def test_products_delete_view(self):
        
        product = Product.objects.create(name="Product test")
        url = reverse("products:product_delete", kwargs={"slug": product.slug})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url) 
        self.assertIn("permission_denied", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url) 
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk})) 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
    
    def test_products_details_view(self):
        
        product = Product.objects.create(name="Product test")
        url = reverse("products:product_details", kwargs={"slug": product.slug})

        # login required
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")

        response = self.client.get(url) 
        self.assertIn("permission_denied", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url) 
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
        
        store = Store.objects.create(name="Store test")
        self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk})) 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
