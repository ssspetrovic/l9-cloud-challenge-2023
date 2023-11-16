from django.test import TestCase
from .models import Player, PlayerStats


class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Player.objects.create(player_name='Test Player', position='PG')

    def test_player_name_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('player_name').verbose_name
        self.assertEqual(field_label, 'player\'s  name')

    def test_position_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('position').verbose_name
        self.assertEqual(field_label, 'position')

    def test_games_played_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('games_played').verbose_name
        self.assertEqual(field_label, 'games played')

    def test_player_name_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('player_name').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_player_name(self):
        player = Player.objects.get(id=1)
        expected_object_name = f'{player.player_name}'
        self.assertEqual(str(player), expected_object_name)


class PlayerStatsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.player = Player.objects.create(
            player_name='Test Player', position='PG')
        cls.player_stats_data = {
            "FTM": "10",
            "FTA": "20",
            "2PM": "5",
            "2PA": "10",
            "3PM": "2",
            "3PA": "6",
            "REB": "7",
            "BLK": "1",
            "AST": "3",
            "STL": "2",
            "TOV": "1",
        }
        cls.player_stats = PlayerStats.create_from_csv_row(
            cls.player, cls.player_stats_data)

    def test_ftp_calculation(self):
        self.assertAlmostEqual(self.player_stats.ftp, 50.0, places=1)

    def test_two_pp_calculation(self):
        self.assertAlmostEqual(self.player_stats.two_pp, 50.0, places=1)

    def test_three_pp_calculation(self):
        self.assertAlmostEqual(self.player_stats.three_pp, 33.3, places=1)

    def test_pts_calculation(self):
        expected_pts = self.player_stats.ftm + 2 * \
            self.player_stats.two_pm + 3 * self.player_stats.three_pm
        self.assertEqual(self.player_stats.pts, expected_pts)

    def test_val_calculation(self):
        expected_val = (self.player_stats.ftm + 2 * self.player_stats.two_pm + 3 * self.player_stats.three_pm +
                        self.player_stats.reb + self.player_stats.blk + self.player_stats.ast + self.player_stats.stl) - (
            self.player_stats.fta - self.player_stats.ftm + self.player_stats.two_pa -
            self.player_stats.two_pm + self.player_stats.three_pa - self.player_stats.three_pm + self.player_stats.to)
        self.assertAlmostEqual(self.player_stats.val, expected_val, places=1)

    def test_efgp_calculation(self):
        expected_efgp = ((self.player_stats.two_pm + self.player_stats.three_pm + 0.5 * self.player_stats.three_pm) /
                         (self.player_stats.two_pa + self.player_stats.three_pa)) * 100
        self.assertAlmostEqual(self.player_stats.efgp, expected_efgp, places=1)

    def test_tsp_calculation(self):
        expected_tsp = (self.player_stats.pts / (2 * (self.player_stats.two_pa +
                        self.player_stats.three_pa + 0.475 * self.player_stats.fta))) * 100
        self.assertAlmostEqual(self.player_stats.tsp, expected_tsp, places=1)

    def test_hastp_calculation(self):
        expected_hastp = (self.player_stats.ast / (self.player_stats.two_pa + self.player_stats.three_pa +
                          0.475 * self.player_stats.fta + self.player_stats.ast + self.player_stats.to)) * 100
        self.assertAlmostEqual(self.player_stats.hastp,
                               expected_hastp, places=1)
