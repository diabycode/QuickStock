from django.db import models
from django.core.exceptions import ValidationError


class Singleton(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    

class EditableSettings(Singleton):
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de l'entreprise")
