# Generated by Django 2.2.1 on 2019-06-17 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0015_auto_20190617_0307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='previous_hash',
            new_name='previous_has',
        ),
    ]
