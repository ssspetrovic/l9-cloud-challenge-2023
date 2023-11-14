from django.contrib import admin

# Register your models here.
from .models import Player, PlayerStats

admin.site.register(Player)
admin.site.register(PlayerStats)