# Generated by Django 2.2.17 on 2020-11-23 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0056_auto_20201118_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='employee_type',
            field=models.CharField(blank=True, choices=[('ADMINISTRATOR', 'Administrator'), ('MANAGER', 'Manager'), ('HR', 'HR')], default=None, max_length=32, null=True, verbose_name='Employee type'),
        ),
        migrations.AddField(
            model_name='user',
            name='employee_type',
            field=models.CharField(blank=True, choices=[('ADMINISTRATOR', 'Administrator'), ('MANAGER', 'Manager'), ('HR', 'HR')], default=None, max_length=32, null=True, verbose_name='Employee type'),
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('phone_number', models.CharField(max_length=16, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
