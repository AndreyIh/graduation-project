# Generated by Django 3.0.5 on 2020-05-16 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0005_auto_20200407_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='genitive_name',
        ),
    ]
