# Generated by Django 2.2.14 on 2020-07-15 08:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20200702_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateCV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cv_file', models.FileField(upload_to='candidate_cvs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_cvs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
