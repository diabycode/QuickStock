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
    

def pin_code_verification(value: str):
    if not len(value) == 4:
        raise ValidationError("Le code pin doit contenir quatre (4) caractères")
    
    if not value.isdigit():
        raise ValidationError("Le code pin doit contenir que des chiffres")


class EditableSettings(Singleton):
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de l'entreprise")
    pin_code = models.CharField(max_length=4, blank=True, null=True, 
                                validators=[pin_code_verification], 
                                verbose_name="Code pin")
