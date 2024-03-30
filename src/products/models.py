from django.db import models
from django.utils.text import slugify


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name="Nom")
    stock_quantity = models.IntegerField(default=0, verbose_name="Quantité en stock")
    wholesale_unit_price = models.FloatField(default=.0, null=True, verbose_name="Prix unitaire gros")
    unit_price_sale = models.FloatField(default=.0, null=True, verbose_name="Prix unitaire vente")
    packaging_type = models.CharField(max_length=100, null=True, verbose_name="Paquetage")
    slug = models.SlugField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name.capitalize()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.pk)
            self.save()
        
