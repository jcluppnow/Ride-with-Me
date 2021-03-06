# Generated by Django 3.2.5 on 2021-08-17 07:41

import application.models.validators
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('full_name', models.CharField(max_length=255)),
                ('profile', models.ImageField(null=True, upload_to='uploads/profile_images')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('average_speed', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('route_coordinates', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('name', models.TextField()),
                ('max_participants', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(null=True)),
                ('starting_time', models.DateTimeField(validators=[application.models.validators.validate_start_time])),
                ('is_private', models.BooleanField()),
                ('starting_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('hero_image', models.ImageField(null=True, upload_to='uploads/hero_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('check_ins', models.ManyToManyField(related_name='check_ins', to=settings.AUTH_USER_MODEL)),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organiser', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL)),
            ],
        )
    ]
