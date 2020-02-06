import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

"""It is possible to run custom code from django project from shell by passing it as an argument to manage.py:
- python manage.py CUSTOM_COMMAND
Here the CUSTOM_COMMAND is "wait_for_db" such that we want to wait for database connection before running server."""

class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    
    # Overwrite handle method in django.core.management.base.BaseCommand
    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                # get the database with keyword 'default' from settings.py
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
        