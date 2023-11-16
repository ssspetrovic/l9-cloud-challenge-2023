from django.db import models


class Player(models.Model):
    """
    Django model for a basketball player.

    This class represents a basketball player with a name, position, and the number of games they've played.
    The player's position is one of the following: Point guard (PG), Shooting guard (SG), Small forward (SF), Power forward (PF), or Center (C).

    Attributes:
        player_name (CharField): The name of the player. This field cannot be null.
        position (CharField): The position of the player. This field can only take one of the predefined choices in POSITIONS.
        games_played (IntegerField): The number of games the player has played. This field defaults to 0.
        CSV_MAPPING (dict): A dictionary mapping CSV column names to model field names.
    """
    POSITIONS = [
        ("PG", "Point guard"),
        ("SG", "Shooting guard"),
        ("SF", "Small forward"),
        ("PF", "Power forward"),
        ("C", "Center")
    ]

    player_name = models.CharField(
        max_length=50, null=False, verbose_name="player's  name")
    position = models.CharField(max_length=2, choices=POSITIONS)
    games_played = models.IntegerField(default=0, verbose_name="games played")

    CSV_MAPPING = {
        "PLAYER": "player_name",
        "POSITION": "position",
    }

    @classmethod
    def create_from_csv_row(cls, row):
        """
        Django model for a basketball player.

        This class represents a basketball player with attributes for their name, position, and the number of games they've played. The player's position is one of the predefined choices. The class also includes a mapping from CSV column names to model field names for data import.
        """
        player_data = {cls.CSV_MAPPING[key]: value for key,
                       value in row.items() if key in cls.CSV_MAPPING}
        player, _ = cls.objects.get_or_create(**player_data)
        return player

    def __str__(self):
        return self.player_name


class PlayerStats(models.Model):
    """
    Django model for a player's statistics.

    This class represents a player's statistics in a basketball game. It includes base statistics such as free throws made and attempted, two-point shots made and attempted, three-point shots made and attempted, rebounds, blocks, assists, steals, and turnovers.

    It also includes derived statistics which are calculated based on the base statistics. These include free throw percentage, two-point percentage, three-point percentage, points, valuation, effective field goal percentage, true shooting percentage, and assist to turnover ratio.
    """
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="statistics")

    # Base statistics
    ftm = models.FloatField(default=0.0, verbose_name="free throw made")
    fta = models.FloatField(default=0.0, verbose_name="free throw attempted")
    two_pm = models.FloatField(default=0.0, verbose_name="two points made")
    two_pa = models.FloatField(
        default=0.0, verbose_name="two points attempted")
    three_pm = models.FloatField(default=0.0, verbose_name="three points made")
    three_pa = models.FloatField(
        default=0.0, verbose_name="three points attempted")
    reb = models.FloatField(default=0.0, verbose_name="rebounds")
    blk = models.FloatField(default=0.0, verbose_name="blocks")
    ast = models.FloatField(default=0.0, verbose_name="assists")
    stl = models.FloatField(default=0.0, verbose_name="steals")
    to = models.FloatField(default=0.0, verbose_name="turnovers")

    # Derived statistics
    @property
    def ftp(self):
        return round((self.ftm / self.fta) * 100 if self.fta else 0, 1)

    @property
    def two_pp(self):
        return round((self.two_pm / self.two_pa) * 100 if self.two_pa else 0, 1)

    @property
    def three_pp(self):
        return round((self.three_pm / self.three_pa) * 100 if self.three_pa else 0, 1)

    @property
    def pts(self):
        return self.ftm + 2 * self.two_pm + 3 * self.three_pm

    @property
    def val(self):
        return round((self.ftm + 2 * self.two_pm + 3 * self.three_pm + self.reb + self.blk + self.ast + self.stl) - (self.fta - self.ftm + self.two_pa - self.two_pm + self.three_pa - self.three_pm + self.to), 1)

    @property
    def efgp(self):
        return round(((self.two_pm + self.three_pm + 0.5 * self.three_pm) / (self.two_pa + self.three_pa)) * 100 if (self.two_pa + self.three_pa) else 0, 1)

    @property
    def tsp(self):
        return round((self.pts / (2 * (self.two_pa + self.three_pa + 0.475 * self.fta))) * 100 if (2 * (self.two_pa + self.three_pa + 0.475 * self.fta)) else 0, 1)

    @property
    def hastp(self):
        return round((self.ast / (self.two_pa + self.three_pa + 0.475 * self.fta + self.ast + self.to)) * 100 if (self.two_pa + self.three_pa + 0.475 * self.fta + self.ast + self.to) else 0, 1)

    CSV_MAPPING = {
        "FTM": "ftm",
        "FTA": "fta",
        "2PM": "two_pm",
        "2PA": "two_pa",
        "3PM": "three_pm",
        "3PA": "three_pa",
        "REB": "reb",
        "BLK": "blk",
        "AST": "ast",
        "STL": "stl",
        "TOV": "to",
    }

    @classmethod
    def create_from_csv_row(cls, player, row):
        """
        Class method to create a player's stats from a row of CSV data.

        This method takes a player object and a row of CSV data as input. It creates a dictionary 'stats_data' where
        each key-value pair is a stat and its corresponding value from the CSV row. Only the keys present in 'CSV_MAPPING'
        are considered, and their values are converted to float.

        The 'player' object is then added to 'stats_data', and a new player stat is created in the database using this data.

        After the player stat is successfully created, the 'games_played' count for the player is incremented by 1.

        Args:
            player (Player): The player object for whom the stats are being created.
            row (dict): A dictionary representing a row of CSV data.

        Returns:
            player_stats (PlayerStats): The newly created player stats object.
        """
        stats_data = {cls.CSV_MAPPING[key]: float(value) for key,
                      value in row.items() if key in cls.CSV_MAPPING}
        stats_data["player"] = player
        player_stats = cls.objects.create(**stats_data)

        # After the stat was successfully created, increment the game count
        player.games_played += 1
        player.save()
        return player_stats

    def traditional_to_dict(self):
        """
        Calculate and return the per game traditional statistics of a player rounded to 1 decimal.

        Returns:
            dict: A dictionary containing the per game statistics.
        """
        return {
            "freeThrows": {
                "attempts": round(self.fta, 1),
                "made": round(self.ftm, 1),
                "shootingPercentage": round(self.ftp, 1),
            },
            "twoPoints": {
                "attempts": round(self.two_pa, 1),
                "made": round(self.two_pm, 1),
                "shootingPercentage": round(self.two_pp, 1),
            },
            "threePoints": {
                "attempts": round(self.three_pa, 1),
                "made": round(self.three_pm, 1),
                "shootingPercentage": round(self.three_pp, 1),
            },
            "points": round(self.pts, 1),
            "rebounds": round(self.reb, 1),
            "blocks": round(self.blk, 1),
            "assists": round(self.ast, 1),
            "steals": round(self.stl, 1),
            "turnovers": round(self.to, 1),
        }

    def advanced_to_dict(self):
        """
        Calculate and return the per game advanced statistics of a player rounded to 1 decimal.

        Returns:
            dict: A dictionary containing the per game statistics.
        """
        return {
            "valorization": round(self.val, 1),
            "effectiveFieldGoalPercentage": round(self.efgp, 1),
            "trueShootingPercentage": round(self.tsp, 1),
            "hollingerAssistRatio": round(self.hastp, 1),
        }

    class Meta:
        verbose_name_plural = "player stats"

    def __str__(self):
        return f"{self.player.player_name}'s statistics"
