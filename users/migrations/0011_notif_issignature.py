# Generated by Django 2.2 on 2019-05-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_notif_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='isSignature',
            field=models.BooleanField(default=False),
        ),
    ]