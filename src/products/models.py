from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField(default=0)
    packaging_type = models.CharField(max_length=100, null=True)
    slug = models.SlugField(blank=True, null=True)


