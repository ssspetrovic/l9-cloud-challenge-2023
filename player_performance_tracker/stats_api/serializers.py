from rest_framework import serializers


class PlayerStatsAggregateSerializer(serializers.Serializer):
    playerName = serializers.CharField(source="player.player_name")
    gamesPlayed = serializers.IntegerField(source="player.games_played")
    traditional = serializers.SerializerMethodField()
    advanced = serializers.SerializerMethodField()

    def get_traditional(self, obj):
        return obj.traditional_to_dict()

    def get_advanced(self, obj):
        return obj.advanced_to_dict()
