# Generated by Django 2.2.12 on 2020-05-29 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200526_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn Profile'),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='candidate_images', verbose_name='Profile image'),
        ),
    ]
