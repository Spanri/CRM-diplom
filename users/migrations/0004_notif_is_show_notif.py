# Generated by Django 2.2 on 2019-05-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190526_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='is_show_notif',
            field=models.BooleanField(default=True),
        ),
    ]