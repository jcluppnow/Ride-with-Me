# Generated by Django 3.2.5 on 2021-09-25 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_alter_weather_weather_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='weather',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weather', to='application.weather'),
        ),
    ]
