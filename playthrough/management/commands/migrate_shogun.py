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
        self.stdout.write('- Migrating games...')
        c.execute('SELECT name, channel_suffix, role_name FROM Game')
        games_in_db = c.fetchall()
        self.stdout.write(f'- - Found {len(games_in_db)} games.')
        for game_row in games_in_db:
            self.stdout.write(f'- - Migrating {game_row[0]}')
            role_template = RoleTemplate.objects.create(name=game_row[2])
            game = Game.objects.get_or_create(
                name=game_row[0]
            )[0]
            game.channel_suffix = f'-plays-{game_row[1]}'
            game.completion_role = role_template
            game.save()
            self.stdout.write(f'- - Saved {game_row[0]}.')
            # Migrate Aliases
            c.execute('SELECT alias FROM Game_Alias WHERE game_name = ?', (game.name,))
            aliases = c.fetchall()
            self.stdout.write(f'- - - Found {len(aliases)} aliases.')
            for alias in aliases:
                game.aliases.add(Alias(alias=alias[0]), bulk=False)
            self.stdout.write('- - - Migrated aliases.')
            # Migrate Configs
            c.execute('SELECT Guild_Id FROM Game_Guild WHERE Game_Name = ?', (game.name,))
            configs = c.fetchall()
            self.stdout.write(f'- - - Found {len(configs)} GameConfigs.')
            for config in configs:
                self.stdout.write(f'- - - Migrating {game} - {config[0]}.')
                GameConfig.objects.get_or_create(
                    guild_id=config[0], game=game, playable=True, completion_role_id='000000000000'
                )
            # Migrate Channels
            c.execute('SELECT ID, Owner, Guild FROM Channel WHERE Game = ?', (game.name,))
            channels = c.fetchall()
            self.stdout.write(f'- - - Found {len(channels)} channels.')
            for channel in channels:
                self.stdout.write(f'- - - Migrating {channel[0]}...')
                user = User.objects.get_or_create(id=channel[1])[0]
                Channel.objects.get_or_create(id=channel[0], owner=user, guild_id=channel[2], game=game)
                self.stdout.write(f'- - - Migrated {channel[0]}.')
