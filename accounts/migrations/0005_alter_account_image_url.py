# Generated by Django 5.0.6 on 2024-07-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_account_birth_date_remove_account_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image_url',
            field=models.CharField(blank=True, default='https://i.ibb.co/XsJCM4t/image-placeholder-icon-11.png', max_length=250, null=True),
        ),
    ]
