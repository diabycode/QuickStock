import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.urls import reverse

from accounts.models import UserModel
from debts.models import Debt


class DebtViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_superuser(username="test_user", password="12345")
    
    def test_debt_list_view(self):
        url = reverse("debts:debt_list")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_debt_details_view(self):
        debt = Debt.objects.create(
            granted_by = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_details", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_debt_create_view(self):
        url = reverse("debts:debt_create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_debt_update_view(self):
        debt = Debt.objects.create(
            granted_by = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_update", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)        

    def test_debt_repayment_view(self):
        debt = Debt.objects.create(
            granted_by = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_repayment", kwargs={"debt_pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_debt_delete_view(self):
        debt = Debt.objects.create(
            granted_by = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_delete", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)