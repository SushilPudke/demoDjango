# Generated by Django 2.2.12 on 2020-05-26 11:16

from django.db import migrations

from ..models import User as UserModel


def rename_user_types(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    for user in User.objects.all():
        user.user_type = UserModel.USER_TYPE_COMPANY if user.user_type in ('1', 1) else UserModel.USER_TYPE_CANDIDATE
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200526_1116'),
    ]

    operations = [
        migrations.RunPython(rename_user_types),
    ]
