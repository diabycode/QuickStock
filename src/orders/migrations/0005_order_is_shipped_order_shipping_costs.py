# Generated by Django 5.0.3 on 2024-03-29 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_costs',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
