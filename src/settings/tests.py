from django.test import TestCase, Client
from django.urls import reverse

from settings.models import EditableSettings


class SettingViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_settings_update_view(self):
        url = reverse("settings:setting_update")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)