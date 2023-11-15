from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlayerStatsAggregateSerializer
from .services import PlayerStatsService
from .models import Player
# from .services import DataService

class PlayerStatsView(APIView):
    def get(self, request, player_name):
        # DataService.fill_in_memory_db()
        try:
            aggregated_data = PlayerStatsService.get_aggregated_stats(
                player_name)
            stats = PlayerStatsService.create_stats_from_aggregated(
                aggregated_data)
            serializer = PlayerStatsAggregateSerializer(stats)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({"detail": f"Player with name '{player_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
