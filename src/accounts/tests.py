from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group

from accounts.models import UserModel, UserPreference


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

    def test_action_logs_view(self):
        self.user = UserModel.objects.create_user(username="user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", email="almamy@gmail.com", password="12345")

        url = reverse("accounts:action_logs")

        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_details_view(self):
        # details
        self.user = UserModel.objects.create_user(username="user", password="12345")

        url = reverse("accounts:details")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_update_view(self):
        self.user = UserModel.objects.create_user(username="user", password="12345")

        url = reverse("accounts:update")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)


class AccountCRUDTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_create_user(self):
        user = UserModel.objects.create_user(username="test_user")
        self.assertEqual(UserModel.objects.filter(username=user.username).exists(), True)
        self.assertEqual(UserPreference.objects.filter(user=user).exists(), True)


class UserViewsRenderingTest(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", email="almamy@gmail.com", password="12345")

    def test_user_list_view(self):
        url = reverse("accounts:user_list")
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_user_details_view(self):
        url = reverse("accounts:user_details", kwargs={"pk": self.user.pk})
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_user_create_view(self):
        url = reverse("accounts:user_create")
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_user_update_view(self):
        url = reverse("accounts:user_update", kwargs={"pk": self.user.pk})
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_user_delete_view(self):
        url = reverse("accounts:user_delete", kwargs={"pk": self.user.pk})
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_change_user_password(self):
        url = reverse("accounts:change_user_password", kwargs={"pk": self.user.pk})
        
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)


class GroupViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(username="user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", email="almamy@gmail.com", password="12345")

    def test_group_list_view(self):
        url = reverse("accounts:group_list")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_group_create_view(self):
        url = reverse("accounts:group_create")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_group_update_view(self):
        group = Group.objects.create(name="group")
        url = reverse("accounts:group_update", kwargs={"pk": group.pk})
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

    def test_group_delete_view(self):
        group = Group.objects.create(name="group")
        url = reverse("accounts:group_delete", kwargs={"pk": group.pk})
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/login/", rp.url)

        self.client.login(username=self.user.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 302)
        self.assertIn("/permission_denied/", rp.url)

        self.client.login(username=self.superuser.username, password="12345")
        rp = self.client.get(url)
        self.assertEqual(rp.status_code, 200)

