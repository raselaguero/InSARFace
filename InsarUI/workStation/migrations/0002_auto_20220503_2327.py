# Generated by Django 3.2.9 on 2022-05-03 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='address',
            field=models.CharField(default='desconocida', max_length=100),
        ),
        migrations.AddField(
            model_name='investigator',
            name='company',
            field=models.CharField(default='desconocida', max_length=100),
        ),
        migrations.AddField(
            model_name='investigator',
            name='country',
            field=models.CharField(default='desconocido', max_length=30),
        ),
    ]
