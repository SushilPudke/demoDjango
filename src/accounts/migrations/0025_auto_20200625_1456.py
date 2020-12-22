# Generated by Django 2.2.13 on 2020-06-25 11:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20200625_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_description',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(255, message='Please enter minimum 255 symbols')], verbose_name='Description'),
        ),
    ]
