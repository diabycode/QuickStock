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
    company_logo = models.ImageField(upload_to="settings/", verbose_name="Logo entreprise",
                                     blank=True, null=True)

    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"
        default_permissions = []
        permissions = [
            ("can_add_setting", "Ajouter - Paramètre"),
            ("can_change_setting", "Modifier - Paramètre"),
            ("can_delete_setting", "Supprimer - Paramètre"),
            ("can_view_setting", "Voir - Paramètre"),
        ]
    
    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name