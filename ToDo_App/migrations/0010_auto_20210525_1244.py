# Generated by Django 2.2 on 2021-05-25 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_App', '0009_auto_20210525_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
    ]
