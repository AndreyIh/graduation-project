# Generated by Django 3.0.4 on 2020-04-09 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trains', '0002_auto_20200407_1449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['name'], 'verbose_name': 'Поезд', 'verbose_name_plural': 'Поезда'},
        ),
    ]
