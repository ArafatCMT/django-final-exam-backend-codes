# Generated by Django 5.0.6 on 2024-07-16 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='account',
            name='relationship',
        ),
    ]
