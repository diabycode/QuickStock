import datetime
import pytz

from django.test import TestCase, Client
from django.urls import reverse
from django.urls import reverse

from accounts.models import UserModel
from debts.models import Debt, DebtRepayment


class DebtViewsRenderingTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create(username="test_user", password="12345")
        self.superuser = UserModel.objects.create_superuser(username="superuser", password="12345")
    
    def test_debt_list_view(self):
        url = reverse("debts:debt_list")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        # logged in
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/permission_denied/", response.url)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_debt_details_view(self):
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_details", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_debt_create_view(self):
        url = reverse("debts:debt_create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_debt_update_view(self):
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_update", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)        

    def test_debt_repayment_view(self):
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_repayment", kwargs={"debt_pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_debt_delete_view(self):
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(),
            initial_amount = 12000.00,
        )
        url = reverse("debts:debt_delete", kwargs={"pk": debt.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_debt_repayment_edit(self):

        # edit_repayment
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(pytz.UTC),
            initial_amount = 12000.00,
        )
        repayment = DebtRepayment.objects.create(
            debt=debt,
            paid_at=datetime.datetime.now(pytz.UTC)
        )
        url = reverse("debts:edit_repayment", kwargs={
            "debt_pk": debt.pk,
            "repayment_pk": repayment.pk
        })
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_debt_repayment_delete(self):
        # repayment_delete
        debt = Debt.objects.create(
            person_concerned = "Almamy Code",
            granted_date = datetime.datetime.now(pytz.UTC),
            initial_amount = 12000.00,
        )
        repayment = DebtRepayment.objects.create(
            debt=debt,
            paid_at=datetime.datetime.now(pytz.UTC)
        )
        url = reverse("debts:repayment_delete", kwargs={
            "debt_pk": debt.pk,
            "repayment_pk": repayment.pk
        })
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
        self.client.login(username=self.user.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.superuser.username, password="12345")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
