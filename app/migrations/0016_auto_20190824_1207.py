# Generated by Django 2.2.2 on 2019-08-24 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20190822_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 24, 12, 7, 49, 746253), verbose_name='Дата регистрации'),
        ),
    ]
