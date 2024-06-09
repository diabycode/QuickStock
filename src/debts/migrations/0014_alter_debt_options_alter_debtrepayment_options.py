# Generated by Django 5.0.3 on 2024-06-05 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0013_alter_debtrepayment_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debt',
            options={'default_permissions': [], 'permissions': [('can_add', 'Ajouter - Impayé'), ('can_change', 'Modifier - Impayé'), ('can_delete', 'Supprimer - Impayé'), ('can_view', 'Voir - Impayé')], 'verbose_name': 'Impayé', 'verbose_name_plural': 'Impayés'},
        ),
        migrations.AlterModelOptions(
            name='debtrepayment',
            options={'default_permissions': [], 'permissions': [('can_add', "Ajouter - Reboursement d'Impayé"), ('can_change', "Modifier - Reboursement d'Impayé"), ('can_delete', "Supprimer - Reboursement d'Impayé"), ('can_view', "Voir - Reboursement d'Impayé")], 'verbose_name': "Remboursement d'Impayé", 'verbose_name_plural': "Remboursements d'Impayé"},
        ),
    ]
