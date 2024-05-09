# Generated by Django 5.0.3 on 2024-05-02 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_usermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Adresse mail'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=80, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=80, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=80, unique=True, verbose_name="Nom d'utilisateur"),
        ),
    ]