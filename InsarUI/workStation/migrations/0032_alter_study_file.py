# Generated by Django 3.2.9 on 2022-09-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0031_alter_study_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='imports/'),
        ),
    ]
