# Generated by Django 2.2 on 2019-09-20 04:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point_of_sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_expired',
            field=models.DateField(default=datetime.date(2019, 9, 20), verbose_name='Ημερομηνία'),
        ),
    ]
