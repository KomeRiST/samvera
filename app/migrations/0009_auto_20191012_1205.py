# Generated by Django 2.2.2 on 2019-10-12 07:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20191012_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 12, 12, 5, 41, 68083), verbose_name='Дата регистрации'),
        ),
    ]