# Generated by Django 2.2.6 on 2020-02-17 14:20

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0003_auto_20191104_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='eng_url',
            field=models.URLField(blank=True, null=True, verbose_name='Παραμπομή για την Αγγλική Εκδοση.'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='text',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Σχόλια'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Παραπομπή για την Ελληνική Εκδοση.'),
        ),
    ]
