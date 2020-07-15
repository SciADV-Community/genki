import pytest
from django.core.exceptions import ValidationError

from playthrough.models import Guild, Series, Game, RoleTemplate

from . import PlaythroughTestBase


class TestGuild(PlaythroughTestBase):
    @staticmethod
    def create_guild(_id: str = '344862360927993859') -> Guild:
        return Guild.objects.create(id=_id)

    def test_create(self):
        guild_id = '123456789'
        guild = self.create_guild(guild_id)
        assert guild.id == guild_id
        assert guild.pk == guild_id
        assert str(guild) == guild_id


class TestSeries(PlaythroughTestBase):
    @staticmethod
    def create_series(name: str = 'Science Adventure') -> Series:
        return Series.objects.create(name=name)

    def test_create(self):
        series_name = 'Nasuverse'
        series = self.create_series(series_name)
        assert series.name == series_name
        assert series.pk == series_name
        assert str(series) == series_name


class TestRoleTemplate(PlaythroughTestBase):
    @staticmethod
    def create_role_template(
        name: str = 'Chaos Child', colour: str = '13817d'
    ) -> RoleTemplate:
        return RoleTemplate.objects.create(name=name, colour=colour)

    def test_create(self):
        role_name = 'Chaos;Head Noah'
        role_colour = '0000FF'
        role_template = self.create_role_template(role_name, role_colour)
        assert role_template.name == role_name
        assert role_template.colour == role_colour
        assert str(role_template) == role_name

    def test_invalid_colour(self):
        role_name = 'Chaos;Head Noah'
        role_colour = '000000FF'
        with pytest.raises(ValidationError):
            template = self.create_role_template(role_name, role_colour)
            template.full_clean()
        role_colour = 'invali'
        with pytest.raises(ValidationError):
            template = self.create_role_template(role_name, role_colour)
            template.full_clean()


class TestGame(PlaythroughTestBase):
    @staticmethod
    def create_game(
        name: str = 'ChäoS;Child', series_name: str = 'Science Adventure'
    ) -> Game:
        series = TestSeries.create_series(series_name)
        return Game.objects.create(name=name, series=series)

    def test_create(self):
        game_name = 'Witch in the Holy Night'
        series_name = 'Nasuverse'
        game = self.create_game(game_name, series_name)
        series = Series.objects.get(name=series_name)
        completion_role = TestRoleTemplate.create_role_template()
        assert game.name == game_name
        assert game.pk == game_name
        assert str(game) == game_name
        assert game.series == series
        assert len(series.games.all()) > 0
        assert game.completion_role is None
        game.completion_role = completion_role
        game.save()
        completion_role.refresh_from_db()
        assert completion_role.game == game
        assert game.completion_role == completion_role

    def test_game_relations(self):
        game = self.create_game()
        series = Series.objects.get(name='Science Adventure')
        game2 = Game.objects.create(series=series, name='ChäoS;HEAd')
        game.prequels.add(game2)
        game2.refresh_from_db()
        assert len(game.prequels.all()) > 0
        assert len(game2.sequels.all()) > 0
