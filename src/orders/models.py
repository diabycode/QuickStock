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
    # is_shipped = models.BooleanField(default=False, blank=True, verbose_name="Livré")
    shipping_costs = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name="Frais de livraison")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, verbose_name="Produit")
    quantity = models.PositiveIntegerField(default=0, null=True, verbose_name="Quantité")
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS, verbose_name="Livraison")
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")
    added_to_stock = models.BooleanField(default=False)
    add_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        default_permissions = []
        permissions = [
            ("can_add_order", "Ajouter - Commande"),
            ("can_change_order", "Modifier - Commande"),
            ("can_delete_order", "Supprimer - Commande"),
            ("can_view_order", "Voir - Commande"),
        ]
    
    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    def __str__(self) -> str:
        return f"{self.product.name} : {self.order_date.strftime('%d-%m-%Y')}"
    
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
            
    @property
    def is_shipped(self):
        return self.status == OrderStatus.SHIPPED