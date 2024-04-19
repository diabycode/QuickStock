# Generated by Django 5.0.3 on 2024-04-06 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_sale_status'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.store', verbose_name='Magasin'),
        ),
    ]
