# Generated by Django 2.2 on 2021-05-24 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_App', '0004_auto_20210523_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='day',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
