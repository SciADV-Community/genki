import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from playthrough.models import (
    Guild, Series, RoleTemplate, Game, User, Channel, Category,
    GameConfig, MetaRoleTemplate, Archive, Alias
)

from . import PlaythroughTestBase
from .utils import get_xml_file


class TestUser(PlaythroughTestBase):
    @staticmethod
    def create_user(_id: str = '93043948775305216') -> User:
        return User.objects.get_or_create(id=_id)[0]

    def test_create(self):
        user_id = '1234567891234567'
        user = self.create_user(user_id)
        assert user.id == user_id
        assert user.pk == user_id
        assert str(user) == user_id
        assert not user.bot_admin
        user.bot_admin = True
        user.save()
        assert user.bot_admin


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

    def test_admins(self):
        user = TestUser.create_user()
        guild = self.create_guild()
        guild.admins.add(user)
        assert len(guild.admins.all()) > 0
        assert guild.admins.all()[0].id == user.id

    def test_games(self):
        guild = self.create_guild()
        game = GameConfig.objects.create(
            game=Game.objects.create(name='Test Game'),
            guild=guild, completion_role_id='406495229743595520'
        )
        guild.games.add(game)
        assert len(guild.games.all()) > 0


class TestSeries(PlaythroughTestBase):
    @staticmethod
    def create_series(name: str = 'Science Adventure') -> Series:
        return Series.objects.get_or_create(name=name)[0]

    def test_create(self):
        series_name = 'Nasuverse'
        series = self.create_series(series_name)
        assert series.name == series_name
        assert series.pk != series_name
        assert series.slug == 'nasuverse'
        assert str(series) == series_name

    def test_aliases(self):
        series = self.create_series()
        series.aliases.add(Alias(alias='sciadv'), bulk=False)
        assert len(series.aliases.all()) > 0
        assert Series.get_by_name_or_alias('sciadv') is not None
        with pytest.raises(Series.DoesNotExist):
            Series.get_by_name_or_alias('tm')


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
        name: str = 'ChäoS;Child',
        series_name: str = 'Science Adventure',
        channel_suffix: str = None
    ) -> Game:
        series = TestSeries.create_series(series_name)
        return Game.objects.create(
            name=name, series=series, channel_suffix=channel_suffix
        )

    def test_create(self):
        game_name = 'Witch in the Holy Night'
        series_name = 'Nasuverse'
        game = self.create_game(game_name, series_name)
        series = Series.objects.get(name=series_name)
        completion_role = TestRoleTemplate.create_role_template()
        assert game.name == game_name
        assert game.pk != game_name
        assert str(game) == game_name
        assert game.slug == 'witch-in-the-holy-night'
        assert game.channel_suffix == '-plays-witch-in-the-holy-night'
        assert game.series == series
        assert len(series.games.all()) > 0
        assert game.completion_role is None
        game.completion_role = completion_role
        game.save()
        completion_role.refresh_from_db()
        assert completion_role.game == game
        assert game.completion_role == completion_role

    def test_slug_unique_guard(self):
        self.create_game('Chaos;Child')
        with pytest.raises(IntegrityError):
            self.create_game('ChaoS;ChilD')

    def test_create_with_channel_suffix(self):
        game_name = 'Witch in the Holy Night'
        series_name = 'Nasuverse'
        game = self.create_game(game_name, series_name, '-plays-wothn')
        assert game.channel_suffix == '-plays-wothn'

    def test_game_relations(self):
        game = self.create_game()
        series = Series.objects.get(name='Science Adventure')
        game2 = Game.objects.create(series=series, name='ChäoS;HEAd')
        game.prequels.add(game2)
        game2.refresh_from_db()
        assert len(game.prequels.all()) > 0
        assert len(game2.sequels.all()) > 0

    def test_aliases(self):
        game = self.create_game()
        game.aliases.add(Alias(alias='c;c'), bulk=False)
        assert len(game.aliases.all()) > 0
        assert Game.get_by_name_or_alias('c;c') is not None
        with pytest.raises(Game.DoesNotExist):
            Game.get_by_name_or_alias('other')


class TestCategory(PlaythroughTestBase):
    @staticmethod
    def create_category(_id: str = '599079485639229440') -> Category:
        guild = TestGuild.create_guild()
        return Category.objects.create(id=_id, guild=guild)

    def test_create(self):
        category_id = '373025048740626433'
        category = self.create_category(category_id)
        assert category.id == category_id
        assert category.pk == category_id
        assert category.guild is not None
        assert str(category) == category_id


class TestGameConfig(PlaythroughTestBase):
    @staticmethod
    def create_game_config(role_id: str = '406495229743595520') -> GameConfig:
        game = TestGame.create_game()
        category = TestCategory.create_category()
        return GameConfig.objects.create(
            guild=category.guild, game=game, category=category,
            completion_role_id=role_id
        )

    def test_create(self):
        role_id = '421657085000810507'
        game_config = self.create_game_config(role_id)
        assert game_config.category is not None
        assert game_config.guild is not None
        assert game_config.game is not None
        assert game_config.completion_role_id == role_id
        assert str(game_config) == f'{game_config.guild} - {game_config.game}'


class TestChannel(PlaythroughTestBase):
    @staticmethod
    def create_channel(_id: str = '499636879554117642') -> Channel:
        game = TestGame.create_game()
        user = TestUser.create_user()
        guild = TestGuild.create_guild()
        return Channel.objects.get_or_create(
            id=_id, owner=user, game=game, guild=guild
        )[0]

    def test_create(self):
        channel_id = '499672300291883008'
        channel = self.create_channel(channel_id)
        assert channel.id == channel_id
        assert channel.pk == channel_id
        assert channel.guild is not None
        assert channel.owner is not None
        assert channel.game is not None
        assert str(channel) == channel_id


class TestMetaRoleTemplate(PlaythroughTestBase):
    @staticmethod
    def create_metaroletemplate(
        name: str = 'Child Head', expr: str = 'test1&&test2'
    ) -> MetaRoleTemplate:
        return MetaRoleTemplate.objects.create(name=name, expression=expr)

    def test_create(self):
        role = self.create_metaroletemplate()
        game1 = TestGame.create_game(name='Game 1')
        game2 = TestGame.create_game(name='Game 2')
        role.games.add(game1, game2)
        assert len(role.games.all()) == 2
        assert role.expression is not None


class TestArchive(PlaythroughTestBase):
    @staticmethod
    def create_archive():
        channel = TestChannel.create_channel()
        file = get_xml_file()
        return Archive.objects.create(channel=channel, file=file)

    def test_create(self):
        archive = self.create_archive()
        assert archive.file is not None
        channel = Channel.objects.get(pk=archive.channel.id)
        assert channel.archive is not None
        user = TestUser.create_user()
        archive.users.add(user)
        assert len(archive.users.all()) > 0
