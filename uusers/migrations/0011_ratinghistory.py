# Generated by Django 2.1 on 2018-09-04 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uusers', '0010_auto_20180830_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to='uusers.UserDetail')),
            ],
        ),
    ]
