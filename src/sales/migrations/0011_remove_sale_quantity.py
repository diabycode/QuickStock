# Generated by Django 5.0.3 on 2024-06-12 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_remove_sale_product_saleproduct_sale_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
    ]