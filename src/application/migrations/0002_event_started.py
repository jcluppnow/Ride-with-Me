# Generated by Django 3.2.5 on 2021-08-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
