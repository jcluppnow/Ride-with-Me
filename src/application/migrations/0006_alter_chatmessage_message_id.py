# Generated by Django 3.2.5 on 2021-09-20 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='message_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
