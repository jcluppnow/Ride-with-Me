# Generated by Django 3.2.5 on 2021-08-20 14:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_event_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='average_speed',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
