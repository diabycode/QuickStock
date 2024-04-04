# Generated by Django 5.0.3 on 2024-03-31 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Quantité en stock'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price_sale',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Prix unitaire vente'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Prix unitaire gros'),
        ),
    ]
