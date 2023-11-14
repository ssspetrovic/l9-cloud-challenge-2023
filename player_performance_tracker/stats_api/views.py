from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Player, PlayerStats


# Create your views here.
def index(response):
    player, created = Player.objects.get_or_create(
        player_name="Leeroy Jankins")
    if created:
        return HttpResponse("No luck!")

    stats = player.statistics.first()
    return JsonResponse(stats.to_dict())
