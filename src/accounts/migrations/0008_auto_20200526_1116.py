# Generated by Django 2.2.12 on 2020-05-26 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0007_auto_20200521_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('COMPANY', 'Company'), ('CANDIDATE', 'Candidate')], default='CANDIDATE',
                                   max_length=32, verbose_name='User type'),
        ),
    ]
