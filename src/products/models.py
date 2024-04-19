from django.db import models
from django.utils.text import slugify


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name="Nom du produit")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    wholesale_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Prix unitaire gros")
    unit_price_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Prix unitaire vente")
    packaging_type = models.CharField(max_length=100, null=True, verbose_name="Paquetage", blank=True)
    slug = models.SlugField(blank=True, null=True)
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")

    stock_warn_limit = 10
    stock_alert_limit = 5

    def __str__(self) -> str:
        return f"{self.name.capitalize()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.pk)
            self.save()
        
    @property
    def stock_alert(self):
        if self.stock_quantity <= self.stock_alert_limit:
            return "alert"
        if self.stock_quantity <= 10:
            return "warn"