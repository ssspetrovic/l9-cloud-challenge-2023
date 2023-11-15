from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Player, PlayerStats
from .services import fill_db_from_csv
from .serializers import PlayerStatsSerializer


class PlayerStatsViewSet(ViewSet):
    fill_db_from_csv()
    def retrieve(self, request, player_name=None):
        queryset = PlayerStats.objects.filter(player__player_name=player_name)
        serializer = PlayerStatsSerializer(queryset, many=True)
        return Response(serializer.data)
    