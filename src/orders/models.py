from django.db import models

from orders.signals import order_shipped_signal, order_cancelled_signal


class OrderStatus(models.TextChoices):
    IN_PROGRESS = ("0", "En cours")
    SHIPPED = ("1", "Livré")
    CANCELLED = ("2", "Annulé")


class Order(models.Model):
    provider_name = models.CharField(max_length=150, verbose_name="Nom du fournisseur", blank=True)
    provider_phone = models.CharField(max_length=30, verbose_name="Téléphone du fournisseur", blank=True)
    order_date = models.DateField(auto_now_add=True, blank=True, verbose_name="Date de commande")
    arrived_date = models.DateField(null=True, blank=True, verbose_name="Date de livraison")    
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    is_shipped = models.BooleanField(default=False, blank=True, verbose_name="Livré")
    shipping_costs = models.FloatField(default=.0, null=True, verbose_name="Frais de livraison")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, verbose_name="Produit")
    quantity = models.PositiveIntegerField(default=0, null=True, verbose_name="Quantité")
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS)
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")

    def __str__(self) -> str:
        return f"Order from {self.provider_name}"
    
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