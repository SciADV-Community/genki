"""Database models for the playthrough app."""
from django.db import models

from genki.validators import hex_validator


class Guild(models.Model):
    """A model to represent a Discord guild."""
    #: The Discord ID of the Guild.
    id = models.CharField(
        max_length=255, db_index=True, unique=True, primary_key=True,
        help_text='The Guild\'s Discord ID.'
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
        help_text='The Series\' name in English.'
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
        max_length=100, db_index=True, help_text='The role\'s name in English.'
    )
    colour = models.CharField(
        max_length=6, help_text='The role\'s colour in hex.', validators=[hex_validator]
    )

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
        help_text='The Game\'s name in English.'
    )
    #: The game's series.
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='games')
    #: The game's prequels.
    prequels = models.ManyToManyField(
        'self', related_name='sequels', blank=True, symmetrical=False
    )
    #: The game's completion role.
    completion_role = models.OneToOneField(
        RoleTemplate, on_delete=models.SET_NULL, null=True, related_name='game'
    )

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the game.
        """
        return self.name


__all__ = [
    'Guild', 'Series',
    'Game', 'RoleTemplate'
]
