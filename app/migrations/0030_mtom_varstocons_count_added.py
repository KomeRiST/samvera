# Generated by Django 2.2.6 on 2020-01-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20200125_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='mtom_varstocons',
            name='count_added',
            field=models.BooleanField(default=False),
        ),
    ]