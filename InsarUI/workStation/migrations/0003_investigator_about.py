# Generated by Django 3.2.9 on 2022-05-03 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0002_auto_20220503_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='about',
            field=models.TextField(default='desconocido', max_length=250),
        ),
    ]
