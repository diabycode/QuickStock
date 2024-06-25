import decimal
import datetime

from django.db import models
from unidecode import unidecode

from sales.signals import sale_cancelled_signal


class SaleStatus(models.TextChoices):
    VALIDATED = ("1", "Validé")
    CANCELLED = ("2", "Annulé")


class SaleProduct(models.Model):
    sale = models.ForeignKey("Sale", on_delete=models.CASCADE, verbose_name="Vente")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(default=1, verbose_name="Quantité vendu")
    is_locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    @property
    def total(self):
        return self.product.unit_price_sale * self.quantity

    class Meta:
        verbose_name = "Produit de la vente"
        verbose_name_plural = "Produits de la vente"
        unique_together = ('sale', 'product')


class Sale(models.Model):
    sale_date = models.DateField(verbose_name="Date de vente")
    products = models.ManyToManyField("products.Product", through="SaleProduct", verbose_name="Produits vendus")
    buyer_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom de l'acheteur")
    buyer_phone = models.CharField(max_length=100, null=True, blank=True, verbose_name="Téléphone de l'acheteur")
    status = models.CharField(max_length=30, choices=SaleStatus.choices, default=SaleStatus.VALIDATED, verbose_name="Statut")
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, null=True, verbose_name="Magasin")
    add_at = models.DateTimeField(auto_now_add=True, null=True)
    seller = models.ForeignKey("accounts.UserModel", on_delete=models.SET_NULL, verbose_name="Vendeur", null=True)

    def __str__(self) -> str:
        return f"Vente : {self.sale_date.strftime('%d-%m-%Y')}"

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        default_permissions = []
        permissions = [
            ("can_add_sale", "Ajouter - Vente"),
            ("can_change_sale", "Modifier - Vente"),
            ("can_delete_sale", "Supprimer - Vente"),
            ("can_view_sale", "Voir - Vente"),
        ]

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name
    
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
        total = decimal.Decimal(0.00)
        for saleproduct in self.saleproduct_set.all():
            total += saleproduct.total
        return total
    
    @property
    def income(self):
        income = decimal.Decimal(0.00)
        for saleproduct in self.saleproduct_set.all():
            i = (saleproduct.product.unit_price_sale - saleproduct.product.wholesale_unit_price) * saleproduct.quantity
            income += i
        return income

    @property
    def unaccent_buyer_name(self):
        return unidecode(self.buyer_name) if self.buyer_name else None
    
    @classmethod
    def get_day_sale_number(cls, store):
        today = datetime.datetime.now().date()
        return Sale.objects.filter(store=store, sale_date__day=today.day, sale_date__month=today.month, sale_date__year=today.year).count()
    
    @classmethod
    def get_day_sale_revenue(cls, store):
        today = datetime.datetime.now().date()
        day_sales =  Sale.objects.filter(store=store, sale_date__day=today.day, sale_date__month=today.month, sale_date__year=today.year)
        
        day_revenue = decimal.Decimal(0.00)
        for sale in day_sales:
            sale_revenue = decimal.Decimal(0.00)
            for saleproduct in sale.saleproduct_set.all():
                product_revenue = saleproduct.product.unit_price_sale * saleproduct.quantity
                sale_revenue += product_revenue
            day_revenue += sale_revenue
        return day_revenue

    @classmethod
    def get_day_sale_product_quantity(cls, store):
        today = datetime.datetime.now().date()
        day_sales =  Sale.objects.filter(store=store, sale_date__day=today.day, sale_date__month=today.month, sale_date__year=today.year)
        
        total_quantity = 0
        for sale in day_sales:
            for saleproduct in sale.saleproduct_set.all():
                total_quantity += saleproduct.quantity
        return total_quantity
