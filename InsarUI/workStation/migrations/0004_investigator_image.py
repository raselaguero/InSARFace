# Generated by Django 3.2.9 on 2022-05-04 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0003_investigator_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='image',
            field=models.ImageField(default='static_files/img/perfil1.png', upload_to='perfil'),
        ),
    ]