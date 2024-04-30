from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import UserModel


class AccountViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
    
    def test_account_login_view(self):
        url = reverse("accounts:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/register/", response.url)

        user = UserModel.objects.create_superuser(username="superuser", password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=user.username, password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_account_register_view(self):
        url = reverse("accounts:register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertIn("/register/", response.url)

        user = UserModel.objects.create_superuser(username="superuser", password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=user.username, password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_account_logout(self):
        url = reverse("accounts:logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        user = UserModel.objects.create_superuser(username="superuser", password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=user.username, password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

