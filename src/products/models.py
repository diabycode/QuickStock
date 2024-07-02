import datetime
import decimal

from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name="Nom du produit")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    wholesale_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Prix unitaire gros")
    unit_price_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Prix unitaire vente")
    packaging_type = models.CharField(max_length=100, null=True, verbose_name="Paquetage", blank=True)
    slug = models.SlugField(blank=True, null=True)
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")
    
    add_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Ajouté le")

    stock_warn_limit = 10
    stock_alert_limit = 5

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        default_permissions = []
        permissions = [
            ("can_add_product", "Ajouter - Produit"),
            ("can_change_product", "Modifier - Produit"),
            ("can_delete_product", "Supprimer - Produit"),
            ("can_view_product", "Voir - Produit"),
        ]

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name
    
    def __str__(self) -> str:
        return f"{self.name.capitalize()} (Qte: {self.stock_quantity})"
    
    def __repr__(self) -> str:
        return f"<Product: {self.name} ({self.stock_quantity})>"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.pk)
            self.save()

    def get_sales(self, month=None, year=None):
        month = datetime.datetime.now().month if not month else month
        year = datetime.datetime.now().year if not year else year
        return self.sale_set.filter(sale_date__month=month, sale_date__year=year)
    
    def get_sales_count(self, from_date: datetime.date, to_date: datetime.date):
        total_sale = 0
        saleproducts = self.saleproduct_set.all().filter(sale__add_at__range=[from_date, to_date])
        for saleproduct in saleproducts:
            total_sale += saleproduct.quantity
        return total_sale
    
    def get_recent_sales(self, month=None, year=None):
        month = datetime.datetime.now().month if not month else month
        year = datetime.datetime.now().year if not year else year
        return self.saleproduct_set.all().filter(sale__add_at__month=month, sale__add_at__year=year).order_by("-sale__add_at")

    @property
    def unaccent_name(self):
        return unidecode(self.name)

    @property
    def stock_alert(self):
        if self.stock_quantity <= self.stock_alert_limit:
            return "alert"
        if self.stock_quantity <= 10:
            return "warn"