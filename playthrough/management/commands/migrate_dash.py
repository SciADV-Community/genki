import os
import sqlite3
import argparse

from django.core.management.base import BaseCommand

from playthrough.models import Channel, Game, GameConfig, Guild, RoleTemplate, User

class Command(BaseCommand):
    help = 'Migrates a DB from \'DaSH\' bot (legacy bot used in Gate of Zero).'

    @staticmethod
    def _db_path(path: str):
        if os.path.isfile(path) and path.endswith('.sqlite'):
            return path
        else:
            raise argparse.ArgumentTypeError(f'{path} is not a valid path to an SQLite Database.')

    def add_arguments(self, parser):
        parser.add_argument('sqlite_file', type=self._db_path)

    def handle(self, *args, **options):
        GUILD_ID = '480817692350218250'
        Guild.objects.get_or_create(id=GUILD_ID, name="Gate of Zero")

        conn = sqlite3.connect((options['sqlite_file']))
        c = conn.cursor()

        self.stdout.write(f'- Migrating channels...')
        c.execute('SELECT userID, gameName, gameRoom, name FROM rooms')
        channel_list = c.fetchall()
        self.stdout.write(f'- - Found {len(channel_list)} channels in the database.')

        for channel in channel_list:
            self.stdout.write(f'- - Migrating channel {channel[2]} ({channel[1]})')

            # Assign username
            user = User.objects.get_or_create(id=channel[0])[0]
            user.username = channel[3]
            user.save()

            # Fetch or create game
            game = Game.objects.get_or_create(
                name=channel[1]
            )[0]

            # Create channel
            Channel.objects.get_or_create(id=channel[2], owner=user, guild_id=GUILD_ID, game=game)
            self.stdout.write(f'- - Migrated channel {channel[2]} successfully.')

        c.close()
