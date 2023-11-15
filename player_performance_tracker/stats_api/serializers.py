from django.db.models import Avg
from rest_framework import serializers
from .models import PlayerStats

class FreeThrowsSerializer(serializers.Serializer):
    attempts = serializers.FloatField(source="fta")
    made = serializers.FloatField(source="ftm")
    shootingPercentage = serializers.ReadOnlyField(source="ftp")

class TwoPointsSerializer(serializers.Serializer):
    attempts = serializers.FloatField(source="two_pa")
    made = serializers.FloatField(source="two_pm")
    shootingPercentage = serializers.ReadOnlyField(source="two_pp")

class ThreePointsSerializer(serializers.Serializer):
    attempts = serializers.FloatField(source="three_pa")
    made = serializers.FloatField(source="three_pm")
    shootingPercentage = serializers.ReadOnlyField(source="three_pp")

class TraditionalSerializer(serializers.Serializer):
    freeThrows = FreeThrowsSerializer(source="*")
    twoPoints = TwoPointsSerializer(source="*")
    threePoints = ThreePointsSerializer(source="*")
    points = serializers.ReadOnlyField(source="pts")
    rebounds = serializers.FloatField(source="reb")
    blocks = serializers.FloatField(source="blk")
    assists = serializers.FloatField(source="ast")
    steals = serializers.FloatField(source="stl")
    turnovers = serializers.FloatField(source="to")

class AdvancedSerializer(serializers.Serializer):
    valorization = serializers.ReadOnlyField(source="val")
    effectiveFieldGoalPercentage = serializers.ReadOnlyField(source="efgp")
    trueShootingPercentage = serializers.ReadOnlyField(source="tsp")
    hollingerAssistRatio = serializers.ReadOnlyField(source="hastp")

class PlayerStatsSerializer(serializers.ModelSerializer):
    playerName = serializers.CharField(source="player.player_name")
    gamesPlayed = serializers.IntegerField(source="player.games_played")
    traditional = TraditionalSerializer(source="*")
    advanced = AdvancedSerializer(source="*")

    class Meta:
        model = PlayerStats
        fields = ["playerName", "gamesPlayed", "traditional", "advanced"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        player_stats = PlayerStats.objects.filter(player__player_name=instance.player.player_name)
        
        # Calculate the average for each field
        games_played_avg = player_stats.aggregate(Avg('player__games_played'))['player__games_played__avg']
        attempts_fta_avg = player_stats.aggregate(Avg('fta'))['fta__avg']
        made_ftm_avg = player_stats.aggregate(Avg('ftm'))['ftm__avg']
        attempts_two_pa_avg = player_stats.aggregate(Avg('two_pa'))['two_pa__avg']
        made_two_pm_avg = player_stats.aggregate(Avg('two_pm'))['two_pm__avg']
        attempts_three_pa_avg = player_stats.aggregate(Avg('three_pa'))['three_pa__avg']
        made_three_pm_avg = player_stats.aggregate(Avg('three_pm'))['three_pm__avg']
        rebounds_avg = player_stats.aggregate(Avg('reb'))['reb__avg']
        blocks_avg = player_stats.aggregate(Avg('blk'))['blk__avg']
        assists_avg = player_stats.aggregate(Avg('ast'))['ast__avg']
        steals_avg = player_stats.aggregate(Avg('stl'))['stl__avg']
        turnovers_avg = player_stats.aggregate(Avg('to'))['to__avg']
        
        # Calculate the averages for the properties
        pts_avg = sum([stat.pts for stat in player_stats]) / len(player_stats)
        val_avg = sum([stat.val for stat in player_stats]) / len(player_stats)
        efgp_avg = sum([stat.efgp for stat in player_stats]) / len(player_stats)
        tsp_avg = sum([stat.tsp for stat in player_stats]) / len(player_stats)
        hastp_avg = sum([stat.hastp for stat in player_stats]) / len(player_stats)

        # Create a new dictionary for aggregated values
        aggregated_data = {
            'gamesPlayed': games_played_avg,
            'traditional': {
                'freeThrows': {
                    'attempts': attempts_fta_avg,
                    'made': made_ftm_avg,
                    'shootingPercentage': made_ftm_avg / attempts_fta_avg * 100 if attempts_fta_avg else 0
                },
                'twoPoints': {
                    'attempts': attempts_two_pa_avg,
                    'made': made_two_pm_avg,
                    'shootingPercentage': made_two_pm_avg / attempts_two_pa_avg * 100 if attempts_two_pa_avg else 0
                },
                'threePoints': {
                    'attempts': attempts_three_pa_avg,
                    'made': made_three_pm_avg,
                    'shootingPercentage': made_three_pm_avg / attempts_three_pa_avg * 100 if attempts_three_pa_avg else 0
                },
                'points': pts_avg,
                'rebounds': rebounds_avg,
                'blocks': blocks_avg,
                'assists': assists_avg,
                'steals': steals_avg,
                'turnovers': turnovers_avg,
            },
            'advanced': {
                'valorization': val_avg,
                'effectiveFieldGoalPercentage': efgp_avg,
                'trueShootingPercentage': tsp_avg,
                'hollingerAssistRatio': hastp_avg,
            },
        }

        return aggregated_data

