from django.test import TestCase
from .models import Player


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
