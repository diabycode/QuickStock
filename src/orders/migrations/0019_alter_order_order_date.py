# Generated by Django 5.0.3 on 2024-05-21 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_order_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2024, 5, 21, 11, 57, 4, 23196, tzinfo=datetime.timezone.utc), verbose_name='Date de commande'),
        ),
    ]