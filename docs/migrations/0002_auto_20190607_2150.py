# Generated by Django 2.2.1 on 2019-06-07 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doc',
            old_name='fileCabinet',
            new_name='file_cabinet',
        ),
    ]
