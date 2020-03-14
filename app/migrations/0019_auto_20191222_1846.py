# Generated by Django 2.2.6 on 2019-12-22 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_tovar_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tovar',
            name='collection',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collectionparts', to='app.Collection', verbose_name='В составе коллекции'),
        ),
    ]