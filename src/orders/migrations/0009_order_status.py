# Generated by Django 5.0.3 on 2024-04-01 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', 'En cours'), ('1', 'Livré'), ('2', 'Annulé')], default='0', max_length=30),
        ),
    ]
