# Generated by Django 5.0.3 on 2024-03-31 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_name_alter_product_packaging_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nom du produit'),
        ),
    ]
