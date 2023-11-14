from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Player(models.Model):
    POSITIONS = [
        ("PG ", "Point guard"),
        ("SG", "Shooting guard"),
        ("SF", "Smallforward"),
        ("PF", "Power forward"),
        ("C", "Center")
    ]

    playerName = models.CharField(
        max_length=20, null=False, verbose_name="player's  name")
    position = models.CharField(max_length=2, choices=POSITIONS)


class PlayerStats(models.Model):
    # Regular statistics
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0)

    ft_attempts = models.FloatField(default=0.0)
    ft_made = models.FloatField(default=0.0)
    ft_percentage = models.FloatField(default=0.0)

    two_pt_attempts = models.FloatField(default=0.0)
    two_pt_made = models.FloatField(default=0.0)
    two_pt_percentage = models.FloatField(default=0.0)

    three_pt_attempts = models.FloatField(default=0.0)
    three_pt_made = models.FloatField(default=0.0)
    three_pt_percentage = models.FloatField(default=0.0)

    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)

    # Advanced statistics
    valorization = models.FloatField(default=0.0)
    effective_field_goal_percentage = models.FloatField(default=0.0)
    true_shooting_percentage = models.FloatField(default=0.0)
    hollinger_assist_ratio = models.FloatField(default=0.0)
