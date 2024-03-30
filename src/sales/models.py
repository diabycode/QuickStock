from django.db import models


class Sale(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    sale_date = models.DateField()


