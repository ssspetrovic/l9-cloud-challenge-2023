import os
import logging
import csv

from django.core.management import call_command
from django.db import connections
from django.db.utils import OperationalError
from stats_api.models import Player

from django.db.models import Avg
from .models import Player, PlayerStats


class DataService:
    FILE_PATH = "stats_api/data/L9HomeworkChallengePlayersInput.csv"
    MODE = "r"
    ENCODING = "utf-8-sig"

    REQUIRED_COLUMNS = ["PLAYER", "POSITION", "FTM", "FTA", "2PM",
                        "2PA", "3PM", "3PA", "REB", "BLK", "AST", "STL", "TOV"]

    @staticmethod
    def validate_csv_file():
        if not os.path.exists(DataService.FILE_PATH):
            logging.error(
                f"File {DataService.FILE_PATH} does not exist.")
            raise FileNotFoundError(
                f"File {DataService.FILE_PATH} does not exist.")
        try:
            with open(file=DataService.FILE_PATH,  mode=DataService.MODE, encoding=DataService.ENCODING) as csv_file:
                reader = csv.DictReader(csv_file)
                if not set(DataService.REQUIRED_COLUMNS).issubset(reader.fieldnames):
                    logging.error("CSV file is missing required columns.")
                    raise ValueError("CSV file is missing required columns.")
        except Exception as e:
            logging.error(f"Error opening file {
                          DataService.FILE_PATH}: {str(e)}")
            raise

    @staticmethod
    def fill_db_from_csv():
        try:
            DataService.validate_csv_file()
            with open(file=DataService.FILE_PATH, mode=DataService.MODE, encoding=DataService.ENCODING) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    player = Player.create_from_csv_row(row)
                    PlayerStats.create_from_csv_row(player, row)
        except Exception as e:
            logging.error(f"Error filling database from CSV: {str(e)}")
            raise


class PlayerStatsService:
    @staticmethod
    def get_aggregated_stats(player_name):
        player = Player.objects.get(player_name=player_name)
        aggregation_fields = {f"avg_{field}": Avg(
            field) for field in PlayerStats.CSV_MAPPING.values()}
        aggregated_data = PlayerStats.objects.filter(
            player=player).aggregate(**aggregation_fields)
        aggregated_data["player"] = player
        return aggregated_data

    @staticmethod
    def create_stats_from_aggregated(aggregated_data):
        stats = PlayerStats()
        for field in PlayerStats.CSV_MAPPING.values():
            if hasattr(stats, field):
                setattr(stats, field, aggregated_data[f"avg_{field}"])
        stats.player = aggregated_data["player"]
        return stats
