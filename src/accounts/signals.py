from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserModel, UserPreference


@receiver(signal=post_save, sender=UserModel)
def handle_user_profile_create(sender, instance: UserModel, **kwargs):
    if not UserPreference.objects.filter(user=instance).exists():
        UserPreference.objects.create(user=instance)



