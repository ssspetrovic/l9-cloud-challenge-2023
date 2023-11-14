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


