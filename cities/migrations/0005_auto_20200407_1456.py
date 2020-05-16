# Generated by Django 3.0.4 on 2020-04-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0004_city_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='foto',
        ),
        migrations.AddField(
            model_name='city',
            name='genitive_name',
            field=models.CharField(max_length=250, null=True, verbose_name='Название города в родительном падеже'),
        ),
    ]
