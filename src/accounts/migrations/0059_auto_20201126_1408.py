# Generated by Django 2.2.17 on 2020-11-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_merge_20201123_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='membership_activated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='membership_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='membership_activated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='membership_active',
            field=models.BooleanField(default=False),
        ),
    ]