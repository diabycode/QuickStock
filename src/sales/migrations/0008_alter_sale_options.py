# Generated by Django 5.0.3 on 2024-06-05 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_alter_sale_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'default_permissions': [], 'permissions': [('can_add', 'Ajouter - Vente'), ('can_change', 'Modifier - Vente'), ('can_delete', 'Supprimer - Vente'), ('can_view', 'Voir - Vente')], 'verbose_name': 'Vente', 'verbose_name_plural': 'Ventes'},
        ),
    ]