from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Player, PlayerStats
from .services import fill_db_from_csv
from django.views import View
from django.db.models import Avg

class PlayerStatsView(View):
    fill_db_from_csv()
    def get(self, request, player_name):
        # Retrieve the player or return 404 if not found
        player = get_object_or_404(Player, player_name=player_name)

        # Retrieve all game statistics for the player
        player_stats_list = PlayerStats.objects.filter(player=player)

        # Calculate average statistics using Django's Avg aggregate function
        avg_stats = player_stats_list.aggregate(
            avg_ftm=Avg('ftm'),
            avg_fta=Avg('fta'),
            avg_two_pm=Avg('two_pm'),
            avg_two_pa=Avg('two_pa'),
            avg_three_pm=Avg('three_pm'),
            avg_three_pa=Avg('three_pa'),
            avg_reb=Avg('reb'),
            avg_blk=Avg('blk'),
            avg_ast=Avg('ast'),
            avg_stl=Avg('stl'),
            avg_to=Avg('to'),
        )

        # Calculate additional derived statistics
        avg_stats['shooting_percentage'] = round((avg_stats['avg_ftm'] / avg_stats['avg_fta']) * 100 if avg_stats['avg_fta'] else 0, 1)
        avg_stats['points'] = round(avg_stats['avg_ftm'] + 2 * avg_stats['avg_two_pm'] + 3 * avg_stats['avg_three_pm'], 1)

        # Create the response dictionary
        response_data = {
            "playerName": player.player_name,
            "gamesPlayed": player_stats_list.count(),
            "traditional": {
                "freeThrows": {
                    "attempts": avg_stats['avg_fta'],
                    "made": avg_stats['avg_ftm'],
                    "shootingPercentage": avg_stats['shooting_percentage'],
                },
                "twoPoints": {
                    "attempts": avg_stats['avg_two_pa'],
                    "made": avg_stats['avg_two_pm'],
                    "shootingPercentage": round((avg_stats['avg_two_pm'] / avg_stats['avg_two_pa']) * 100 if avg_stats['avg_two_pa'] else 0, 1),
                },
                "threePoints": {
                    "attempts": avg_stats['avg_three_pa'],
                    "made": avg_stats['avg_three_pm'],
                    "shootingPercentage": round((avg_stats['avg_three_pm'] / avg_stats['avg_three_pa']) * 100 if avg_stats['avg_three_pa'] else 0, 1),
                },
                "points": avg_stats['points'],
                "rebounds": avg_stats['avg_reb'],
                "blocks": avg_stats['avg_blk'],
                "assists": avg_stats['avg_ast'],
                "steals": avg_stats['avg_stl'],
                "turnovers": avg_stats['avg_to'],
            },
            "advanced": {
                "valorization": round((avg_stats['avg_ftm'] + 2 * avg_stats['avg_two_pm'] + 3 * avg_stats['avg_three_pm'] + avg_stats['avg_reb'] + avg_stats['avg_blk'] + avg_stats['avg_ast'] + avg_stats['avg_stl']) - (avg_stats['avg_fta'] - avg_stats['avg_ftm'] + avg_stats['avg_two_pa'] - avg_stats['avg_two_pm'] + avg_stats['avg_three_pa'] - avg_stats['avg_three_pm'] + avg_stats['avg_to']), 1),
                "effectiveFieldGoalPercentage": round(((avg_stats['avg_two_pm'] + avg_stats['avg_three_pm'] + 0.5 * avg_stats['avg_three_pm']) / (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa'])) * 100 if (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa']) else 0, 1),
                "trueShootingPercentage": round((avg_stats['points'] / (2 * (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa'] + 0.475 * avg_stats['avg_fta']))) * 100 if (2 * (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa'] + 0.475 * avg_stats['avg_fta'])) else 0, 1),
                "hollingerAssistRatio": round((avg_stats['avg_ast'] / (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa'] + 0.475 * avg_stats['avg_fta'] + avg_stats['avg_ast'] + avg_stats['avg_to'])) * 100 if (avg_stats['avg_two_pa'] + avg_stats['avg_three_pa'] + 0.475 * avg_stats['avg_fta'] + avg_stats['avg_ast'] + avg_stats['avg_to']) else 0, 1),
            }
        }

        return JsonResponse(response_data)
