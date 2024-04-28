from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import login
from django.urls import reverse

from accounts.models import UserModel
from products.views import ProductListView


class ProductCRUDTest(TestCase):
    pass

        