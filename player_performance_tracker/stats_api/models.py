from django.db import models

# Create your models here.
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
        max_length=20, null=False, verbose_name="player's  name")
    position = models.CharField(max_length=2, choices=POSITIONS)

    def __str__(self):
        return f"{self.player_name} ({self.position})"


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0)
    # Regular statistics
    ftm = models.FloatField(default=0.0, verbose_name="free throw made")
    fta = models.FloatField(default=0.0, verbose_name="free throw attempted")
    two_pm = models.FloatField(default=0.0, verbose_name="two points made")
    two_pa = models.FloatField(default=0.0, verbose_name="two points attempted")
    three_pm = models.FloatField(default=0.0, verbose_name="three points made")
    three_pa = models.FloatField(default=0.0, verbose_name="three points attempted")
    pts = models.FloatField(default=0.0, verbose_name="points")
    reb = models.FloatField(default=0.0, verbose_name="rebounds")
    blk = models.FloatField(default=0.0, verbose_name="blocks")
    ast = models.FloatField(default=0.0, verbose_name="assists")
    stl = models.FloatField(default=0.0, verbose_name="steals")
    to = models.FloatField(default=0.0, verbose_name="turnovers")
    # Derived statistics
    ftp = models.FloatField(default=0.0, verbose_name="free throw percentage")
    two_pp = models.FloatField(default=0.0, verbose_name="two points percentage")
    three_pp = models.FloatField(default=0.0, verbose_name="three points percentage")
    #   Advanced statistics
    val = models.FloatField(default=0.0, verbose_name="valorization")
    efgp = models.FloatField(default=0.0, verbose_name="effective field goal percentage")
    tsp = models.FloatField(default=0.0, verbose_name="true shooting percentage")
    hastp = models.FloatField(default=0.0, verbose_name="hollinger assist ratio")

    class Meta:
        verbose_name_plural = "player stats"

    def __str__(self):
        return f"{self.player.player_name}'s statistics"
    
    