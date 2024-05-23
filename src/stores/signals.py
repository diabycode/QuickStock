from django.db.models.signals import pre_delete
from django.dispatch import receiver

from stores.models import Store


@receiver(pre_delete, sender=Store)
def handle_store_deletion(sender, instance, **kwargs):
    for debt in instance.debt_set.all():
        debt.store_name = instance.name
        debt.store = None
        debt.save()
