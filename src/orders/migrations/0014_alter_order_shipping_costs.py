# Generated by Django 5.0.3 on 2024-05-04 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_order_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_costs',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Frais de livraison'),
        ),
    ]
