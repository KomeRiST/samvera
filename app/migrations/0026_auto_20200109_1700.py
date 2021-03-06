# Generated by Django 2.2.6 on 2020-01-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_mtom_varstocons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mtom_varstocons',
            name='gallery',
        ),
        migrations.AddField(
            model_name='mtom_varstocons',
            name='cost',
            field=models.SmallIntegerField(default=0, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='mtom_varstocons',
            name='nds',
            field=models.SmallIntegerField(default=0, verbose_name='Ставка НДС (%)'),
        ),
        migrations.AddField(
            model_name='mtom_varstocons',
            name='nds_summ',
            field=models.SmallIntegerField(default=0, verbose_name='Сумма НДС (руб.)'),
        ),
        migrations.AddField(
            model_name='mtom_varstocons',
            name='total_nds',
            field=models.SmallIntegerField(default=0, verbose_name='Сумма с учётом НДС'),
        ),
        migrations.AddField(
            model_name='mtom_varstocons',
            name='total_not_nds',
            field=models.SmallIntegerField(default=0, verbose_name='Сумма без НДС'),
        ),
    ]
