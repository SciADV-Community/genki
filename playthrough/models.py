"""Database models for the playthrough app."""
from django.db import models


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

    def __str__(self) -> str:
        """
        Return a string representing the object.

        :return: The name of the game.
        """
        return self.name
