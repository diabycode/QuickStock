# Generated by Django 5.0.3 on 2024-04-27 10:33

import settings.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_rename_settings_editablesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editablesettings',
            name='pin_code',
            field=models.CharField(blank=True, max_length=4, null=True, validators=[settings.models.pin_code_verification], verbose_name='Code pin'),
        ),
    ]