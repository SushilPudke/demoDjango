# Generated by Django 2.2.17 on 2020-11-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_merge_20201027_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='user_type',
            field=models.CharField(choices=[('COMPANY', 'Company'), ('CANDIDATE', 'Candidate'), ('AGENCY', 'Agency'), ('EMPLOYEE', 'Employee')], default='CANDIDATE', max_length=32, verbose_name='User type'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('COMPANY', 'Company'), ('CANDIDATE', 'Candidate'), ('AGENCY', 'Agency'), ('EMPLOYEE', 'Employee')], default='CANDIDATE', max_length=32, verbose_name='User type'),
        ),
    ]