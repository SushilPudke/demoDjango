# Generated by Django 2.2.16 on 2020-10-08 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_auto_20201008_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateprofile',
            name='country_de',
        ),
        migrations.RemoveField(
            model_name='candidateprofile',
            name='country_en',
        ),
        migrations.RemoveField(
            model_name='companyprofile',
            name='country_de',
        ),
        migrations.RemoveField(
            model_name='companyprofile',
            name='country_en',
        ),
    ]
