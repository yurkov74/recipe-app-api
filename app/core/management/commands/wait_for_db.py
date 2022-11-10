"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command for to wait for database."""

    def handle(self, *args, **options):
        """Entry point for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError):
                msg = 'Database is unavailable, waiting 1 second...'
                self.stdout.write(msg)
                time.sleep(1)
            except (OperationalError):
                msg = 'Database is being setting up, waiting 1 second...'
                self.stdout.write(msg)
                time.sleep(1)
            # except Exception:
            #     self.stdout.write('Unnown error occured')

        self.stdout.write(self.style.SUCCESS('Database is ready!'))
