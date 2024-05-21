import datetime

from django.db import models
from django.utils import timezone

from orders.signals import order_shipped_signal, order_cancelled_signal


class OrderStatus(models.TextChoices):
    IN_PROGRESS = ("0", "En cours")
    SHIPPED = ("1", "Livré")
    CANCELLED = ("2", "Annulé")


class Order(models.Model):
    provider_name = models.CharField(max_length=150, verbose_name="Nom du fournisseur", blank=True)
    provider_phone = models.CharField(max_length=30, verbose_name="Téléphone du fournisseur", blank=True)
    order_date = models.DateField(verbose_name="Date de commande", default=timezone.now)
    arrived_date = models.DateField(null=True, blank=True, verbose_name="Date de livraison")    
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    is_shipped = models.BooleanField(default=False, blank=True, verbose_name="Livré")
    shipping_costs = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name="Frais de livraison")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, verbose_name="Produit")
    quantity = models.PositiveIntegerField(default=0, null=True, verbose_name="Quantité")
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS, verbose_name="Livraison")
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")

    add_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.order_date.strftime('%d-%m-%Y')} __{self.product.name}"
    
    @property
    def status_display(self):
        return OrderStatus(self.status).label
    
    @property
    def status_class_name(self):
        match self.status:
            case OrderStatus.SHIPPED:
                return "status validated"
            case OrderStatus.CANCELLED:
                return "status cancelled"
            case OrderStatus.IN_PROGRESS:
                return "status"