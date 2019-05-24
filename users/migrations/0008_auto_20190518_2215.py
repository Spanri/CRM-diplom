# Generated by Django 2.2 on 2019-05-18 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_notif_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='notif',
            name='doc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notif', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notif',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_docs', to=settings.AUTH_USER_MODEL),
        ),
    ]