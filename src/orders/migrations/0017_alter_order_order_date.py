# Generated by Django 5.0.3 on 2024-05-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_order_add_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name='Date de commande'),
        ),
    ]
