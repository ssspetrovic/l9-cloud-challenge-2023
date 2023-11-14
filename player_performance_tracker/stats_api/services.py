import csv
from .models import Player, PlayerStats

FILE_PATH = "stats_api/data/L9HomeworkChallengePlayersInput.csv"
MODE = "r"
ENCODING = "utf-8-sig"


def fill_db_from_csv():
    with open(file=FILE_PATH, mode=MODE, encoding=ENCODING) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            player = Player.create_from_csv_row(row)
            PlayerStats.create_from_csv_row(player, row)
