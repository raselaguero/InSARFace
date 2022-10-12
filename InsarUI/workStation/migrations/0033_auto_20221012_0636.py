# Generated by Django 3.2.9 on 2022-10-12 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workStation', '0032_alter_study_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='displacement',
            name='color',
        ),
        migrations.RemoveField(
            model_name='displacement',
            name='description',
        ),
        migrations.RemoveField(
            model_name='displacement',
            name='name',
        ),
        migrations.AddField(
            model_name='displacement',
            name='velocity',
            field=models.FloatField(blank=True, max_length=20, null=True, verbose_name='Velocidad Vertical'),
        ),
    ]
