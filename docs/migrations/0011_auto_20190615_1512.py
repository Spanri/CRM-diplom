# Generated by Django 2.2.1 on 2019-06-15 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0010_doc_signature_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doc',
            name='signature_text',
        ),
        migrations.AlterField(
            model_name='doc',
            name='signature',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
