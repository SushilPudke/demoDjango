# Generated by Django 2.2.17 on 2020-11-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_merge_20201123_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='position',
            field=models.CharField(default='Hrusha', max_length=255, verbose_name='Last name'),
            preserve_default=False,
        ),
    ]
