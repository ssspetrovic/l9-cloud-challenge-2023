from django.apps import AppConfig

from django.db import connections
from django.core.management import call_command
from django.db.utils import OperationalError


class StatsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats_api'

    def ready(self):
        """
        This method is called when the Django application is ready.

        It attempts to perform a migration on the 'stats_api' app without any user input.
        If the migration is successful, it then calls the 'fill_db_from_csv' method from the 'DataService' class
        in the 'services.py' module to populate the database from a CSV file.

        If the database is not ready (an OperationalError is raised), it prints a message to the console.

        Raises:
            OperationalError: An error occurred while attempting to access the database.
        """
        try:
            call_command('migrate', 'stats_api', '--noinput')
            from .services import DataService
            DataService.fill_db_from_csv()
        except OperationalError:
            print('Database is not ready yet.')
