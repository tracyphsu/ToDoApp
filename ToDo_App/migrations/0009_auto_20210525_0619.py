# Generated by Django 2.2 on 2021-05-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_App', '0008_auto_20210525_0604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start']},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='date',
            new_name='end',
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateField(default='2021-05-21'),
            preserve_default=False,
        ),
    ]