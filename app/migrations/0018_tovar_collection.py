# Generated by Django 2.2.6 on 2019-12-22 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20191222_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='tovar',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='collectionparts', to='app.Collection', verbose_name='Часть коллекции'),
        ),
    ]
