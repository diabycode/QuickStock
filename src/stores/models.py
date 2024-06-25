from django.db import models


class StoreAccentColor(models.TextChoices):
    BLUE = ("#4a75a0", "Bleu")
    PURPLE = ("#a04a8f", "Violet")
    DARK_ORANGE = ("#a06a4a", "Orange sombre")
    DARK_RED = ("#BB4430", "Rouge sombre")
    DARK_BLUE = ("#13293D", "Bleu sombre")
    DARK_ROSE = ("#AA4465", "Rose sombre")
    DARK_PURPLE = ("#474056", "Violet sombre")

    
class StoreCategory(models.TextChoices):
    TELECOM = ("telecom", "Télécommunication")
    BREEDING = ("breeding", "Elevage")
    ELECTRONIC = ("electronic", "Electroménager")
    OTHER = ("other", "Autre")


class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    address = models.CharField(max_length=150, verbose_name="Adresse")
    accent_color_code = models.CharField(max_length=15, null=True, choices=StoreAccentColor.choices,
                                         default=StoreAccentColor.BLUE, verbose_name="Thème")
    category = models.CharField(max_length=150, null=True, choices=StoreCategory.choices,
                                default=StoreCategory.OTHER, verbose_name="Catégorie")
    users = models.ManyToManyField("accounts.UserModel", verbose_name="Accès aux utilisateurs", blank=True)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    add_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Magasin"
        verbose_name_plural = "Magasins"
        default_permissions = []
        permissions = [
            ("can_add_store", "Ajouter - Magasin"),
            ("can_change_store", "Modifier - Magasin"),
            ("can_delete_store", "Supprimer - Magasin"),
            ("can_view_store", "Voir - Magasin"),
            ("can_access_all_store", "Accès à tous les magasins"),
        ]

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def products_count(self):
        return self.product_set.all().count()
