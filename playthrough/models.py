"""Database models for the playthrough app."""
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from genki.models import DiscordIDField, HexColourField

if TYPE_CHECKING:
    from typing import Tuple, Union


class User(models.Model):
    """A model to represent a Discord user."""
    #: The Discord ID of the user.
    id = DiscordIDField(
        db_index=True, unique=True, primary_key=True,
        help_text=_('The User\'s Discord ID.')
    )
    #: Whether or not the user is a bot admin.
    bot_admin = models.BooleanField(
        default=False, help_text=_('Whether or not the User is a bot admin.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The id of the user.
        """
        return self.id


class Alias(models.Model):
    """A model to represent an Alias for a model."""
    #: The alias.
    alias = models.CharField(
        max_length=100, blank=True, unique=True, help_text=_('The Alias.')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        self.alias = self.alias.lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The alias.
        """
        return self.alias


class Guild(models.Model):
    """A model to represent a Discord guild."""
    #: The Discord ID of the Guild.
    id = DiscordIDField(
        db_index=True, unique=True, primary_key=True,
        help_text=_('The Guild\'s Discord ID.')
    )
    #: The guild's bot admins.
    admins = models.ManyToManyField(
        User, related_name='admin_for',
        help_text=_('The Guild\'s bot admins.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The id of the guild.
        """
        return self.id


class Series(models.Model):
    """A model to represent a game series."""
    #: The name of the series.
    name = models.CharField(
        max_length=255, db_index=True,
        help_text=_('The Series\' name.')
    )
    #: The slug of the series. Auto generated.
    slug = models.SlugField(
        unique=True, blank=True,
        help_text=_('The Series\' slug. Auto-generated.')
    )
    #: The series' aliases.
    aliases = GenericRelation(Alias, help_text=_('The Series\' aliases.'))

    @classmethod
    def get_by_name_or_alias(cls, name: str) -> 'Series':
        """Function ot get a Series by its name or alias.

        :return: The series by its alias.
        :raises: Series.DoesNotExist"""
        return Series.objects.get(
            models.Q(name=name) | models.Q(aliases__alias=name.lower())
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'series'

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the series.
        """
        return self.name


class RoleTemplate(models.Model):
    """A model to represent a completion 'role' for a certain game."""
    #: The name of the role.
    name = models.CharField(
        max_length=100, db_index=True, help_text=_('The Role\'s name.')
    )
    colour = HexColourField(
        null=True, blank=True, help_text=_('The Role\'s colour in hex.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the role.
        """
        return self.name

    def get_colour_as_rgb(self) -> 'Union[Tuple[int,int,int],None]':
        """Utility to return the colour in RGB.

        :return: an RGB tuple or None"""
        if self.colour is None:
            return None
        return tuple(int(self.colour[i:i+2], 16) for i in (0, 2, 4))

    def is_valid(self) -> bool:
        """Validate the model.

        :return: Whether or not the object is valid."""
        try:
            self.full_clean()
            return True
        except (ValidationError):
            return False


class Game(models.Model):
    """A model to represent a game."""
    #: The name of the game.
    name = models.CharField(
        max_length=255, db_index=True, unique=True,
        help_text=_('The Game\'s name.')
    )
    #: The game's series.
    series = models.ForeignKey(
        Series, null=True, on_delete=models.SET_NULL, related_name='games',
        help_text=_('The Series the Game belongs to.')
    )
    #: The game's prequels.
    prequels = models.ManyToManyField(
        'self', related_name='sequels', blank=True, symmetrical=False,
        help_text=_('The game\'s prequels.')
    )
    #: The game's completion role.
    completion_role = models.OneToOneField(
        RoleTemplate, on_delete=models.SET_NULL, null=True, related_name='game',
        help_text=_('The role to grant upon game completion.')
    )
    #: The suffix for channels for the game.
    channel_suffix = models.CharField(
        max_length=10, blank=True, help_text=_('The suffix for channels for the game.')
    )
    #: The slug of the game. Auto generated.
    slug = models.SlugField(
        unique=True, blank=True,
        help_text=_('The Game\'s slug. Auto-generated.')
    )
    #: The game's aliases.
    aliases = GenericRelation(Alias, help_text=_('The Game\'s aliases.'))

    @classmethod
    def get_by_name_or_alias(cls, name: str):
        """Function ot get a Game by its name or alias.

        :return: The game by its alias.
        :raises: Game.DoesNotExist"""
        return Game.objects.select_related('completion_role').get(
            models.Q(name=name) | models.Q(aliases__alias=name.lower())
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.channel_suffix:
            self.channel_suffix = f'-plays-{self.slug}'
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the game.
        """
        return self.name


class GameConfig(models.Model):
    """A model to represent a game configured for a guild."""
    #: The game being configured.
    game = models.ForeignKey(
        Game, related_name='configured_with', on_delete=models.CASCADE,
        help_text=_('The Game to configure.')
    )
    #: The guild the configuration is for.
    guild = models.ForeignKey(
        Guild, related_name='games', on_delete=models.CASCADE,
        help_text=_('The Guild to configure for.')
    )
    #: The ID of the Role to grant upon game completion.
    completion_role_id = DiscordIDField(
        help_text=_('The ID of the Role to grant upon game completion.')
    )

    class Meta:
        unique_together = ['game', 'guild']

    def is_valid(self) -> bool:
        """Validate the model.

        :return: Whether or not the object is valid."""
        try:
            self.full_clean()
            return True
        except (ValidationError):
            return False

    @classmethod
    def get_by_game_alias(self, game: str, guild_id: str) -> 'Union[GameConfig,None]':
        try:
            game = Game.get_by_name_or_alias(game)
            try:
                return GameConfig.objects\
                    .select_related('game', 'guild').get(
                        guild_id=guild_id, game=game
                    )
            except (GameConfig.DoesNotExist):
                return None
        except (Game.DoesNotExist):
            return None

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The guild and game name for the configuration.
        """
        return f'{self.guild} - {self.game}'


class Channel(models.Model):
    """A model to represent a Discord playthrough channel."""
    #: The Discord ID of the channel.
    id = DiscordIDField(
        db_index=True, unique=True, primary_key=True,
        help_text=_('The Channel\'s Discord ID.')
    )
    #: The user who owns the channel.
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='channels',
        help_text=_('The owner of the Channel.')
    )
    #: The guild the channel is in.
    guild = models.ForeignKey(
        Guild, on_delete=models.CASCADE, related_name='channels',
        help_text='The Guild the Channel is in.'
    )
    #: The game the channel is for.
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='channels',
        help_text=_('The Game the Channel is for.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The id of the user.
        """
        return self.id


class MetaRoleTemplate(RoleTemplate):
    """A model to represent meta role templates."""
    #: The meta role's expression.
    expression = models.CharField(
        max_length=255, help_text=_('The meta role\'s expression.')
    )
    #: The games the meta role is associated with.
    games = models.ManyToManyField(
        Game, related_name='meta_roles',
        help_text=_('The Games the MetaRole is associated with.')
    )


class Archive(models.Model):
    """A model to represent an archive."""
    def _get_archive_path(instance, filename: str) -> str:
        """Utility function to get the path for an archive file.

        :return: The path for an archive file based on the Archive instance."""
        return f'{instance.channel.id}/{filename}'

    #: The Channel the archive is for.
    channel = models.OneToOneField(
        Channel, related_name='archive', on_delete=models.CASCADE,
        help_text=_('The Channel the archive is for.')
    )
    #: The Users that appear within the archive.
    users = models.ManyToManyField(
        User, related_name='archives',
        help_text=_('The Users that appear within the archive.')
    )
    #: The archive file.
    file = models.FileField(upload_to=_get_archive_path)

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The id of the user.
        """
        return _('Archive for %s' % self.channel)


__all__ = [
    'Guild', 'Series',
    'Game', 'RoleTemplate',
    'User', 'Channel', 'GameConfig',
    'MetaRoleTemplate', 'Archive',
    'Alias'
]
