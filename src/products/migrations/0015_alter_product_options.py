# Generated by Django 5.0.3 on 2024-06-10 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'default_permissions': [], 'permissions': [('can_add_product', 'Ajouter - Produit'), ('can_change_product', 'Modifier - Produit'), ('can_delete_product', 'Supprimer - Produit'), ('can_view_product', 'Voir - Produit')], 'verbose_name': 'Produit', 'verbose_name_plural': 'Produits'},
        ),
    ]
