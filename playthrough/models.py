"""Database models for the playthrough app."""
from django.db import models

from genki.models import DiscordIDField, HexColourField
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    """A model to represent a Discord user."""
    #: The Discord ID of the user.
    id = DiscordIDField(
        db_index=True, unique=True, primary_key=True,
        help_text=_('The User\'s Discord ID.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The id of the user.
        """
        return self.id


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
        max_length=255, db_index=True, unique=True, primary_key=True,
        help_text=_('The Series\' name.')
    )

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
    colour = HexColourField(help_text=_('The Role\'s colour in hex.'))

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the role.
        """
        return self.name


class Game(models.Model):
    """A model to represent a game."""
    #: The name of the game.
    name = models.CharField(
        max_length=255, db_index=True, unique=True, primary_key=True,
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

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the game.
        """
        return self.name


class Category(models.Model):
    """A model to represent a Discord channel category."""
    #: The category's Discord ID.
    id = DiscordIDField(
        db_index=True, unique=True, primary_key=True,
        help_text=_('The Category\'s Discord ID.')
    )
    #: The guild of the category.
    guild = models.ForeignKey(
        Guild, related_name='categories', on_delete=models.CASCADE,
        help_text=_('The Category\'s Guild.')
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The ID of the category.
        """
        return self.id


class GameConfig(models.Model):
    """A model to represent a game configured for a guild."""
    #: The game being configured.
    game = models.ForeignKey(
        Game, related_name='configred_with', on_delete=models.CASCADE,
        help_text=_('The Game to configure.')
    )
    #: The guild the configuration is for.
    guild = models.ForeignKey(
        Guild, related_name='games', on_delete=models.CASCADE,
        help_text=_('The Guild to configure for.')
    )
    #: The category to use for currently active channels.
    category = models.ForeignKey(
        Category, related_name='games', null=True, on_delete=models.SET_NULL,
        help_text=_('The Category for active channels.')
    )
    #: The ID of the Role to grant upon game completion.
    completion_role_id = DiscordIDField(
        help_text=_('The ID of the Role to grant upon game completion.')
    )

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


__all__ = [
    'Guild', 'Series',
    'Game', 'RoleTemplate',
    'User', 'Channel',
    'Category', 'GameConfig'
]
