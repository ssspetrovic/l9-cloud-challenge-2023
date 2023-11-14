from django.db import models


# Create your models here.
class Player(models.Model):
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
        player_data = {cls.CSV_MAPPING[key]: value for key,
                       value in row.items() if key in cls.CSV_MAPPING}
        player, _ = cls.objects.get_or_create(**player_data)
        return player

    def __str__(self):
        return f"{self.player_name} ({self.position})"


class PlayerStats(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="statistics")

    # Regular statistics
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
        stats_data = {cls.CSV_MAPPING[key]: float(value) for key,
                      value in row.items() if key in cls.CSV_MAPPING}
        stats_data["player"] = player
        player_stats = cls.objects.create(**stats_data)

        # After the stat was successfully created, increment the game count
        player.games_played += 1
        player.save()
        return player_stats

    def to_dict(self):
        return {
            "playerName": self.player.player_name,
            "gamesPlayed": self.player.games_played,
            "traditional": {
                "freeThrows": {
                    "attempts": self.fta,
                    "made": self.ftm,
                    "shootingPercentage": self.ftp,
                },
                "twoPoints": {
                    "attempts": self.two_pa,
                    "made": self.two_pm,
                    "shootingPercentage": self.two_pp,
                },
                "threePoints": {
                    "attempts": self.three_pa,
                    "made": self.three_pm,
                    "shootingPercentage": self.three_pp,
                },
                "points": self.pts,
                "rebounds": self.reb,
                "blocks": self.blk,
                "assists": self.ast,
                "steals": self.stl,
                "turnovers": self.to,
            },
            "advanced": {
                "valorization": self.val,
                "effectiveFieldGoalPercentage": self.efgp,
                "trueShootingPercentage": self.tsp,
                "hollingerAssistRatio": self.hastp,
            },
        }

    class Meta:
        verbose_name_plural = "player stats"

    def __str__(self):
        return f"{self.player.player_name}'s statistics"
