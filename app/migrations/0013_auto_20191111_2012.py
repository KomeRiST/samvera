# Generated by Django 2.2.6 on 2019-11-11 20:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20191111_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 11, 20, 12, 43, 445218), verbose_name='Дата регистрации'),
        ),
    ]
