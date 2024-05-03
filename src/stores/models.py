from django.db import models


class StoreAccentColor(models.TextChoices):
    BLUE = ("#4a75a0", "Bleu")
    PURPLE = ("#a04a8f", "Violet")
    DARK_ORANGE = ("#a06a4a", "Orange sombre")
    

class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    address = models.CharField(max_length=150, verbose_name="Adresse")
    accent_color_code = models.CharField(max_length=15, null=True, choices=StoreAccentColor.choices,
                                         default=StoreAccentColor.BLUE, verbose_name="Thème")

    def __str__(self) -> str:
        return self.name