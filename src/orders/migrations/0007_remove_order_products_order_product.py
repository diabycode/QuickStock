# Generated by Django 5.0.3 on 2024-04-01 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_arrived_date_alter_order_description_and_more'),
        ('products', '0007_alter_product_stock_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Produits inclus'),
        ),
    ]
