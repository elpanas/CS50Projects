# Generated by Django 3.1 on 2020-10-15 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beachu', '0005_auto_20201015_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='umb',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 16, 13, 59, 35, 810860)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 15, 13, 59, 35, 810860)),
        ),
    ]
