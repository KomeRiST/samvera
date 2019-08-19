# Generated by Django 2.2.2 on 2019-08-17 15:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190817_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertovaryvariaciya',
            name='variac',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='variaciya', chained_model_field='variaciya', default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Variaciya'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordertovaryvariaciya',
            name='variaciya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='vvvv', to='app.Variaciya'),
        ),
        migrations.AlterField(
            model_name='potentialclient',
            name='data_create',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 17, 20, 55, 19, 5547), verbose_name='Дата регистрации'),
        ),
    ]
