# Generated by Django 3.2.9 on 2022-05-28 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0009_auto_20220528_0349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zone',
            options={'verbose_name_plural': 'Zones'},
        ),
        migrations.RemoveField(
            model_name='zone',
            name='zone_name',
        ),
    ]