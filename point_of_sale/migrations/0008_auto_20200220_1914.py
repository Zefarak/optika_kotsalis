# Generated by Django 2.2.6 on 2020-02-20 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0007_auto_20200219_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.date(2020, 2, 20), verbose_name='Ημερομηνία'),
        ),
    ]