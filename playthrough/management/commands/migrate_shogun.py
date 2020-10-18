import argparse
import os
import sqlite3

from django.core.management.base import BaseCommand

from playthrough.models import Alias, Channel, Game, GameConfig, Guild, RoleTemplate, User


class Command(BaseCommand):
    help = 'Migrates a DB from \'Shogun\' bot (SciADV-Community/playthrough-bot).'

    @staticmethod
    def _db_path(path: str):
        if os.path.isfile(path) and path.endswith('.db'):
            return path
        else:
            raise argparse.ArgumentTypeError(f'{path} is not a valid path to an SQLite Database.')

    def add_arguments(self, parser):
        parser.add_argument('sqlite_file', type=self._db_path)

    def handle(self, *args, **options):
        conn = sqlite3.connect(options['sqlite_file'])
        c = conn.cursor()
        # Migrate Guilds
        c.execute('SELECT Guild_ID, Guild_Name FROM Config')
        guilds_in_db = c.fetchall()
        for guild in guilds_in_db:
            Guild.objects.get_or_create(id=guild[0], name=guild[1])
        # Migrate Games
        c.execute('SELECT name, channel_suffix, role_name FROM Game')
        games_in_db = c.fetchall()
        for game in games_in_db:
            role_template = RoleTemplate.objects.create(name=game[2])
            game = Game.objects.get_or_create(
                name=game[0], channel_suffix=f'-plays-{game[1]}', completion_role=role_template
            )[0]
            # Migrate Aliases
            c.execute('SELECT alias FROM Game_Alias WHERE game_name = ?', (game.name,))
            aliases = c.fetchall()
            for alias in aliases:
                game.aliases.add(Alias(alias=alias[0]), bulk=False)
            # Migrate Configs
            c.execute('SELECT Guild_Id FROM Game_Guild WHERE Game_Name = ?', (game.name,))
            configs = c.fetchall()
            for config in configs:
                GameConfig.objects.get_or_create(
                    guild_id=config[0], game=game, playable=True, completion_role_id='000000000000'
                )
            # Migrate Channels
            c.execute('SELECT ID, Owner, Guild FROM Channel WHERE Game = ?', (game.name,))
            channels = c.fetchall()
            for channel in channels:
                user = User.objects.get_or_create(id=channel[1])[0]
                Channel.objects.get_or_create(id=channel[0], owner=user, guild_id=channel[2], game=game)
