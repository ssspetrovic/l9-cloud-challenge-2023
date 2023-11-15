from django.apps import AppConfig

from django.db import connections
from django.core.management import call_command
from django.db.utils import OperationalError


class StatsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats_api'

    def ready(self):
        try:
            call_command('migrate', 'stats_api', '--noinput')
            from .services import DataService
            DataService.fill_db_from_csv()
        except OperationalError:
            print('Database is not ready yet.')
