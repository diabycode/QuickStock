# Generated by Django 5.0.3 on 2024-03-28 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=150)),
                ('provider_phone', models.CharField(max_length=30)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('arrived_date', models.DateField(null=True)),
            ],
        ),
    ]
