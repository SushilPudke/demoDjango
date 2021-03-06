# Generated by Django 2.2.16 on 2020-10-19 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_auto_20201015_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencyHiring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiring_companies', to='accounts.AgencyProfile')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hired_agencies', to='accounts.CompanyProfile')),
            ],
            options={
                'unique_together': {('company', 'agency')},
            },
        ),
    ]
