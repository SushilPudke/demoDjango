# Generated by Django 2.2.14 on 2020-07-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20200721_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='company_size',
            field=models.IntegerField(blank=True, choices=[(1, '<50'), (2, '50-200'), (3, '200-500'), (4, '500+')], verbose_name='Company Size'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='company_website',
            field=models.URLField(blank=True, max_length=255, verbose_name='Website'),
        ),
    ]