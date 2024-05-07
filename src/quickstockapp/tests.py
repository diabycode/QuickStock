
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import UserModel
from stores.models import Store


class AppViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_superuser(username="Test user", password="12345")
    
    def test_dashbord_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(reverse("home"))
        if response.status_code == 302:
            self.assertIn("/stores/", response.url)
            store = Store.objects.create(name="Store test")
            self.client.get(reverse("stores:change_store", kwargs={"pk": store.pk}))

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


