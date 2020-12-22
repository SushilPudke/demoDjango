# Generated by Django 2.2.15 on 2020-08-06 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_historicaluser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='history_user',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
