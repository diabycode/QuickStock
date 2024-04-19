from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    address = models.CharField(max_length=150, verbose_name="Adresse")

    def __str__(self) -> str:
        return self.name