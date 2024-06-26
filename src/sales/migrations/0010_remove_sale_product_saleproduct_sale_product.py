# Generated by Django 5.0.3 on 2024-06-12 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_product_options'),
        ('sales', '0009_alter_sale_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantité vendu')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Produit')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale', verbose_name='Vente')),
            ],
            options={
                'verbose_name': 'Produit de la vente',
                'verbose_name_plural': 'Produits de la vente',
                'unique_together': {('sale', 'product')},
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='product',
            field=models.ManyToManyField(through='sales.SaleProduct', to='products.product', verbose_name='Produits vendus'),
        ),
    ]