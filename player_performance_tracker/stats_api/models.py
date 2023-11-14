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
        return (self.ftm / self.fta) * 100 if self.fta else 0

    @property
    def two_pp(self):
        return (self.two_pm / self.two_pa) * 100 if self.two_pa else 0

    @property
    def three_pp(self):
        return (self.three_pm / self.three_pa) * 100 if self.three_pa else 0

    @property
    def pts(self):
        return self.ftm + 2 * self.two_pm + 3 * self.three_pm

    @property
    def val(self):
        return (self.ftm + 2 * self.two_pm + 3 * self.three_pm + self.reb + self.blk + self.ast + self.stl) - (self.fta - self.ftm + self.two_pa - self.two_pm + self.three_pa - self.three_pm + self.to)

    @property
    def efgp(self):
        return ((self.two_pm + self.three_pm + 0.5 * self.three_pm) / (self.two_pa + self.three_pa)) * 100 if (self.two_pa + self.three_pa) else 0

    @property
    def tsp(self):
        return (self.pts / (2 * (self.two_pa + self.three_pa + 0.475 * self.fta))) * 100 if (2 * (self.two_pa + self.three_pa + 0.475 * self.fta)) else 0

    @property
    def hastp(self):
        return (self.ast / (self.two_pa + self.three_pa + 0.475 * self.fta + self.ast + self.to)) * 100 if (self.two_pa + self.three_pa + 0.475 * self.fta + self.ast + self.to) else 0

    class Meta:
        verbose_name_plural = "player stats"

    def __str__(self):
        return f"{self.player.player_name}'s statistics"
