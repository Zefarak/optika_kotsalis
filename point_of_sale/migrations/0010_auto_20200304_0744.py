# Generated by Django 2.2 on 2020-03-04 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0009_auto_20200221_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.date(2020, 3, 4), verbose_name='Ημερομηνία'),
        ),
    ]
