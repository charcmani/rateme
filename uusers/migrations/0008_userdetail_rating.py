# Generated by Django 2.1 on 2018-08-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uusers', '0007_userdetail_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
