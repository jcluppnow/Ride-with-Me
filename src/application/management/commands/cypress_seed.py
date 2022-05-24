# pylint: disable=duplicate-code
"""
Seed database if it does not exist or replace with a copy
"""
import os
import shutil

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from application import factories


class Command(BaseCommand):
    """
    Seed database if it does not exist or replace with a copy
    """
    help = 'Seed database if it does not exist or replace with a copy'

    def handle(self, *args, **options):

        verbosity = int(options['verbosity'])

        root_directory = str(settings.BASE_DIR)

        sqlite_name = settings.DATABASES["default"]["NAME"]

        print(f'looking for {sqlite_name}')

        # Check if using sqlite engine
        if settings.DATABASES["default"]["ENGINE"] != 'django.contrib.gis.db.backends.spatialite':
            if verbosity > 0:
                self.stdout.write(
                    "SQLite engine not detected, are you using the correct env? "
                    "See readme for more info"
                )
                self.stdout.write("Migrating and seeding")
            call_command('migrate', verbosity=0)
            Command.seed_db()
        elif os.path.isfile(f'{sqlite_name}.bak'):
            if verbosity > 0:
                self.stdout.write("Backup found, replacing original with copy")
            # If backup file exists then remove original and copy backup to reset the database
            if os.path.isfile(f'{sqlite_name}'):
                os.remove(f'{sqlite_name}')
                shutil.copyfile(
                    f'{sqlite_name}.bak',
                    f'{sqlite_name}'
                )
        else:
            if verbosity > 0:
                self.stdout.write("No backup found, seeding new database")
            # If no backup exists, delete sqlite file
            if os.path.isfile(f'{sqlite_name}'):
                os.remove(f'{sqlite_name}')

            # Flush and Migrate and seed new database
            call_command('flush', '--no-input', verbosity=0)
            call_command('migrate', verbosity=0)
            Command.seed_db()

            # Copy fresh database to backup
            if os.path.isfile(f'{sqlite_name}'):
                shutil.copyfile(
                    f'{sqlite_name}',
                    f'{sqlite_name}.bak'
                )

            with open(
                    f'{root_directory}/application/cypress/fixtures/users.json',
                    'w',
                    encoding="utf-8"
            ) as file:
                call_command('dumpdata', 'application.CustomUser', stdout=file)

            with open(
                    f'{root_directory}/application/cypress/fixtures/events.json',
                    'w',
                    encoding="utf-8"
            ) as file:
                call_command('dumpdata', 'application.Event', stdout=file)

            with open(
                    f'{root_directory}/application/cypress/fixtures/messages.json',
                    'w',
                    encoding="utf-8"
            ) as file:
                call_command(
                    'dumpdata', 'application.ChatMessage', stdout=file)

    def seed_db():  # pylint: disable=no-method-argument
        """
        Seeds the data
        """
        # Instantiate faker
        # Faker.seed(datetime.datetime.now().timestamp())
        # fake = Faker()

        user = factories.UserFactory.create()

        event = factories.EventFactory.create(organiser=user)

        factories.ChatMessageFactory.create_batch(10, event=event)

        # user_ids = []
        #
        # # Seed 10 users
        # for _ in range(10):
        #     user = factories.UserFactory.create()
        #     user_ids.append(user.id)
        #
        # # Seed 4 events
        # for _ in range(4):
        #
        #     # Pick random number of users to act as participants in the event
        #     num_users = fake.random_int(min=2, max=5)
        #     participants = ()
        #     for _ in range(num_users, 5):
        #         participants += (user_ids[fake.random_int(min=0, max=len(user_ids) - 1)],)
        #
        #     factories.EventFactory.create(participants=participants)
