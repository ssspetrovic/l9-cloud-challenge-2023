from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Player, PlayerStats

from .services import fill_db_from_csv

# Create your views here.
def index(response):
    fill_db_from_csv()
    player, created = Player.objects.get_or_create(
        player_name="Jaysee Nkrumah")
    if created:
        return HttpResponse("No luck!")

    stats = player.statistics.first()
    return JsonResponse(stats.to_dict())
