# Generated by Django 3.2.9 on 2022-05-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0005_alter_investigator_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigator',
            name='facebook',
            field=models.URLField(default='https://facebook.com/'),
        ),
        migrations.AddField(
            model_name='investigator',
            name='instagram',
            field=models.URLField(default='https://instagram.com/'),
        ),
        migrations.AddField(
            model_name='investigator',
            name='linkedin',
            field=models.URLField(default='https://linkedin.com/'),
        ),
        migrations.AddField(
            model_name='investigator',
            name='twitter',
            field=models.URLField(default='https://twitter.com/'),
        ),
    ]