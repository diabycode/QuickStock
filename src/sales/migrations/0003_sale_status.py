# Generated by Django 5.0.3 on 2024-04-01 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sale_buyer_name_sale_buyer_phone_sale_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('1', 'Validé'), ('2', 'Annulé')], default='1', max_length=30),
        ),
    ]