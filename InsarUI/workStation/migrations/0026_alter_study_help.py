# Generated by Django 3.2.9 on 2022-06-22 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0025_alter_evidence_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='help',
            field=models.CharField(default='', max_length=1500, verbose_name='Zona'),
        ),
    ]
