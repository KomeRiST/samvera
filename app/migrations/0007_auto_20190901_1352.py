# Generated by Django 2.2.2 on 2019-09-01 08:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190825_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 1, 13, 52, 51, 314213), verbose_name='Дата регистрации'),
        ),
    ]
