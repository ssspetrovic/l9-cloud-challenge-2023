from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlayerStatsAggregateSerializer
from .services import PlayerStatsService
from .models import Player


class PlayerStatsView(APIView):
    """
    API view for handling requests related to player statistics.

    This class provides a GET method to retrieve the aggregated statistics for a player.
    The player's name is expected to be provided in the URL.
    If the player does not exist, a 404 error is returned.

    Attributes:
        get (function): The function to handle GET requests.
    """

    def get(self, request, player_name):
        """
        Handles GET requests for player statistics.

        Retrieves the aggregated statistics for the player with the given name,
        creates a PlayerStats object from the aggregated data,
        serializes the data, and returns it in the response.

        Args:
            request (Request): The GET request.
            player_name (str): The name of the player.

        Returns:
            Response: The response containing the serialized player statistics data,
                      or a 404 error if the player does not exist.
        """
        try:
            aggregated_data = PlayerStatsService.get_aggregated_stats(
                player_name)
            stats = PlayerStatsService.create_stats_from_aggregated(
                aggregated_data)
            serializer = PlayerStatsAggregateSerializer(stats)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({"detail": f"Player with name '{player_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
