# Generated by Django 2.2.2 on 2019-08-25 10:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190824_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertovary',
            name='tovar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orderovary', to='app.Tovar'),
        ),
        migrations.AlterField(
            model_name='ordertovaryvariaciya',
            name='variaciya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ordertovaryvariacii', to='app.Variaciya'),
        ),
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 25, 15, 29, 9, 636566), verbose_name='Дата регистрации'),
        ),
    ]
