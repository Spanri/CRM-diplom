# Generated by Django 2.2.1 on 2019-06-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190611_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='is_notif_expire',
            field=models.BooleanField(default=False),
        ),
    ]
