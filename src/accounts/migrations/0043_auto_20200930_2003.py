# Generated by Django 2.2.16 on 2020-09-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20200922_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('specialization_name', models.CharField(max_length=50, unique=True, verbose_name='Specialization name')),
            ],
            options={
                'verbose_name': 'specialization',
                'verbose_name_plural': 'specializations',
            },
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='specialization',
            field=models.ManyToManyField(related_name='specilaizations', to='accounts.Specialization'),
        ),
        migrations.AddField(
            model_name='technology',
            name='specialization',
            field=models.ManyToManyField(null=True, related_name='technologies', to='accounts.Specialization'),
        ),
    ]
