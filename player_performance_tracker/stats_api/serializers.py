from rest_framework import serializers


class PlayerStatsAggregateSerializer(serializers.Serializer):
    """
    Serializer for the PlayerStatsAggregate model.

    This serializer provides fields for the player's name, the number of games they've played,
    and their traditional and advanced statistics. The traditional and advanced statistics
    are obtained by calling the `traditional_to_dict` and `advanced_to_dict` methods on the
    PlayerStatsAggregate object, respectively.

    Attributes:
        playerName (CharField): The name of the player.
        gamesPlayed (IntegerField): The number of games the player has played.
        traditional (SerializerMethodField): The traditional statistics of the player.
        advanced (SerializerMethodField): The advanced statistics of the player.
    """

    playerName = serializers.CharField(source="player.player_name")
    gamesPlayed = serializers.IntegerField(source="player.games_played")
    traditional = serializers.SerializerMethodField()
    advanced = serializers.SerializerMethodField()

    def get_traditional(self, obj):
        """
        Retrieve the traditional statistics of the player.

        Args:
            obj (PlayerStatsAggregate): The PlayerStatsAggregate object.

        Returns:
            dict: The traditional statistics of the player.
        """
        return obj.traditional_to_dict()

    def get_advanced(self, obj):
        """
        Retrieve the advanced statistics of the player.

        Args:
            obj (PlayerStatsAggregate): The PlayerStatsAggregate object.

        Returns:
            dict: The advanced statistics of the player.
        """
        return obj.advanced_to_dict()
