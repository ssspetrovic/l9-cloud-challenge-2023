from rest_framework import serializers

from .models import Player, PlayerStats


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["player_name", "games_played"]


class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = "__all__"
