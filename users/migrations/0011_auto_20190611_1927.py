# Generated by Django 2.2.1 on 2019-06-11 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_notif_dateexpire'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notif',
            old_name='dateExpire',
            new_name='date_expire',
        ),
    ]