# Generated by Django 3.2.9 on 2022-06-08 17:26

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0014_delete_polylayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionLayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('layer', django.contrib.gis.db.models.fields.GeometryCollectionField(srid=4326)),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workStation.study')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]