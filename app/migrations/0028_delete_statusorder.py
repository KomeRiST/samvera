# Generated by Django 2.2.6 on 2020-01-13 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200113_1745'),
        ('app', '0027_remove_variaciya_kolvo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StatusOrder',
        ),
    ]