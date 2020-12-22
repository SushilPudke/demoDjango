# Generated by Django 2.2.13 on 2020-06-25 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20200625_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateprofile',
            name='cover_letter',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(255, message='Please enter between 255 and 1000 symbols'), django.core.validators.MaxLengthValidator(1000, message='Please enter between 255 and 1000 symbols')], verbose_name='Cover letter'),
        ),
    ]