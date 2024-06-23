from django.test import TestCase, Client
from django.urls import reverse

from settings.models import EditableSettings
from accounts.models import UserModel


class SettingViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="Test user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", password="12345", email="almamy@gmail.com")

    def test_settings_update_view(self):
        url = reverse("settings:setting_update")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertIn("/permission_denied/", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)