# Generated by Django 2.2.6 on 2019-11-11 20:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20191111_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 11, 20, 21, 57, 753160), verbose_name='Дата регистрации'),
        ),
    ]
