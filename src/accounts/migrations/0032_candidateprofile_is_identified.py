# Generated by Django 2.2.14 on 2020-07-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20200721_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='is_identified',
            field=models.BooleanField(default=False, verbose_name='Is identified'),
        ),
    ]