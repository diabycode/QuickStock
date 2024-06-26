# Generated by Django 5.0.3 on 2024-03-29 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_arrived_date'),
        ('products', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(null=True, to='products.product'),
        ),
    ]
