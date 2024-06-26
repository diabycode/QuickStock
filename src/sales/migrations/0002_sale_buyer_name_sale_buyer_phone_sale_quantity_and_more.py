# Generated by Django 5.0.3 on 2024-03-31 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_name'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='buyer_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Nom de l'acheteur"),
        ),
        migrations.AddField(
            model_name='sale',
            name='buyer_phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Téléphone de l'acheteur"),
        ),
        migrations.AddField(
            model_name='sale',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Quantité vendu'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Produit vendu'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateField(verbose_name='Date de vente'),
        ),
    ]
