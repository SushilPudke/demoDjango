# Generated by Django 2.2.12 on 2020-06-03 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_candidateprofile_additional_information'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidateprofile',
            old_name='additional_information',
            new_name='cover_letter',
        ),
    ]
