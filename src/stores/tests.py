from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import UserModel 
from stores.models import Store


class StoreViewsRenderingTest(TestCase):
    # databases = {"default"}

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="Test user", password="12345")

    def test_stores_list_view(self):
        url = reverse("stores:store_list")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        store = Store.objects.create(name="Store test")
        response = self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashbord/", response.url)

    def test_stores_create_view(self):
        url = reverse("stores:store_create")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_stores_update_view(self):
        store = Store.objects.create(name="Store test")
        url = reverse("stores:store_update", kwargs={"pk": store.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_stores_delete_view(self):
        store = Store.objects.create(name="Store test")
        url = reverse("stores:store_delete", kwargs={"pk": store.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/stores/", response.url)



