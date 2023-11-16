import os
import logging
import csv
from django.db.models import Avg
from .models import Player, PlayerStats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataService:
    """
    A service class for handling CSV data and filling the database.

    This class provides methods to validate a CSV file and fill the database with data from the CSV file.
    The CSV file is expected to be in a specific format, with certain required columns.
    """
    FILE_NAME = "L9HomeworkChallengePlayersInput.csv" # TODO Change the name of the file
    FILE_PATH = os.path.join(BASE_DIR, f"stats_api/data/{FILE_NAME}")
    MODE = "r"
    ENCODING = "utf-8-sig"

    REQUIRED_COLUMNS = ["PLAYER", "POSITION", "FTM", "FTA", "2PM",
                        "2PA", "3PM", "3PA", "REB", "BLK", "AST", "STL", "TOV"]

    @staticmethod
    def validate_csv_file():
        """
        Validates the CSV file.

        Checks if the file exists and if it contains the required columns.
        Raises a FileNotFoundError if the file does not exist, and a ValueError if the required columns are missing.
        """
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
        """
        Fills the database with data from the CSV file.

        Validates the CSV file, then reads the file and creates Player and PlayerStats objects for each row.
        Raises an exception if there is an error while filling the database.
        """
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
    """
    A service class for handling player statistics.

    This class provides methods to get aggregated statistics for a player and create PlayerStats objects from aggregated data.
    """
    @staticmethod
    def get_aggregated_stats(player_name):
        """
        Gets the aggregated statistics for a player.

        Args:
            player_name (str): The name of the player.

        Returns:
            dict: A dictionary containing the aggregated statistics for the player.
        """
        player = Player.objects.get(player_name=player_name)
        aggregation_fields = {f"avg_{field}": Avg(
            field) for field in PlayerStats.CSV_MAPPING.values()}
        aggregated_data = PlayerStats.objects.filter(
            player=player).aggregate(**aggregation_fields)
        aggregated_data["player"] = player
        return aggregated_data

    @staticmethod
    def create_stats_from_aggregated(aggregated_data):
        """
        Creates a PlayerStats object from aggregated data.

        Args:
            aggregated_data (dict): A dictionary containing the aggregated data.

        Returns:
            PlayerStats: The created PlayerStats object.
        """
        stats = PlayerStats()
        for field in PlayerStats.CSV_MAPPING.values():
            if hasattr(stats, field):
                setattr(stats, field, aggregated_data[f"avg_{field}"])
        stats.player = aggregated_data["player"]
        return stats
