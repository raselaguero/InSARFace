# Generated by Django 3.2.9 on 2022-06-08 22:11

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0015_collectionlayer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ['munic'], 'verbose_name_plural': 'Municipios'},
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='area',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='areanew',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='arear',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='gid',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='municipio',
            name='the_geom2',
        ),
        migrations.AddField(
            model_name='municipio',
            name='border_col',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='border_sty',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='border_wid',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='cod_munic',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='fill_style',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='layer',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='map_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='municipio',
            name='munic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='municipio',
            name='sup_distkm',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='municipio',
            name='closed',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='municipio',
            name='provincia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
