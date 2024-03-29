from django.db import models


class Order(models.Model):

    provider_name = models.CharField(max_length=150)
    provider_phone = models.CharField(max_length=30)
    order_date = models.DateField(auto_now_add=True, blank=True)
    arrived_date = models.DateField(null=True, blank=True)    
    description = models.TextField(null=True, blank=True)
    is_shipped = models.BooleanField(default=False, blank=True)
    shipping_costs = models.FloatField(default=.0, null=True)
    products = models.ManyToManyField("products.Product", null=True)

    def __str__(self) -> str:
        return f"Order from {self.provider_name}"