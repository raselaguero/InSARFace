# Generated by Django 3.2.9 on 2022-09-01 09:17

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0028_remove_study_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Displacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripcion')),
                ('color', models.CharField(blank=True, max_length=15, null=True, verbose_name='Color')),
                ('altitude', models.FloatField(blank=True, max_length=20, null=True, verbose_name='Altura')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Punto')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('study', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workStation.study')),
            ],
            options={
                'ordering': ['altitude'],
            },
        ),
    ]
