# Generated by Django 5.0.3 on 2024-05-18 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_sale_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='add_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]