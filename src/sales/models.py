from django.db import models
from unidecode import unidecode

from sales.signals import sale_cancelled_signal


class SaleStatus(models.TextChoices):
    VALIDATED = ("1", "Validé")
    CANCELLED = ("2", "Annulé")


class Sale(models.Model):
    sale_date = models.DateField(verbose_name="Date de vente")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, verbose_name="Produit vendu")
    quantity = models.IntegerField(default=1, verbose_name="Quantité vendu")
    buyer_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom de l'acheteur")
    buyer_phone = models.CharField(max_length=100, null=True, blank=True, verbose_name="Téléphone de l'acheteur")
    status = models.CharField(max_length=30, choices=SaleStatus.choices, default=SaleStatus.VALIDATED, verbose_name="Statut")
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock_quantity:
            raise ValueError(f"Quantity sold can't exceed the stock quantity. {self.quantity} > {self.product.stock_quantity}")
        return super().save(*args, **kwargs)
    
    @property
    def status_display(self):
        return SaleStatus(self.status).label
    
    @property
    def status_class_name(self):
        match self.status:
            case SaleStatus.VALIDATED:
                return "status validated"
            case SaleStatus.CANCELLED:
                return "status cancelled"
    
    @property
    def total_amount(self):
        return self.product.unit_price_sale * self.quantity
    
    @property
    def income(self):
        return (self.product.unit_price_sale - self.product.wholesale_unit_price) * self.quantity

    @property
    def unaccent_buyer_name(self):
        return unidecode(self.buyer_name) if self.buyer_name else None
    
    