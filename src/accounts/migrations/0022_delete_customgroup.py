# Generated by Django 5.0.3 on 2024-06-12 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_usermodel_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomGroup',
        ),
    ]