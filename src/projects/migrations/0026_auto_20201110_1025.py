# Generated by Django 2.2.16 on 2020-11-10 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_agencycandidatecv'),
        ('projects', '0025_auto_20201022_1625'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PositionApplication',
            new_name='CandidatePositionApplication',
        ),
        migrations.CreateModel(
            name='AgencyPositionApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_applications', to='accounts.AgencyProfile')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agency_applications', to='projects.Position')),
            ],
            options={
                'unique_together': {('agency', 'position')},
            },
        ),
    ]
