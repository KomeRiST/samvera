# Generated by Django 2.2.2 on 2019-10-13 19:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20191012_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertovaryvariaciya',
            name='order',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.CASCADE, related_name='ordervars', to='app.Orders'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 14, 0, 29, 17, 315186), verbose_name='Дата регистрации'),
        ),
    ]
