# Generated by Django 2.1 on 2018-08-28 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uusers', '0004_auto_20180821_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='total',
        ),
    ]
