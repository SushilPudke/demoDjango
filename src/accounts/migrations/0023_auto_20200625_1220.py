# Generated by Django 2.2.13 on 2020-06-25 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20200625_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateprofile',
            name='cover_letter',
            field=models.TextField(blank=True, max_length=1000, null=True, validators=[django.core.validators.MinLengthValidator], verbose_name='Cover letter'),
        ),
    ]