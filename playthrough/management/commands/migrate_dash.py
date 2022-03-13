import os
import sqlite3
import argparse

from django.core.management.base import BaseCommand

from playthrough.models import Alias, Channel, Game, GameConfig, Guild, RoleTemplate, User

class Command(BaseCommand):

    @staticmethod
    def _db_path(path: str):
        if os.path.isfile(path) and path.endswith('.sqlite'):
            return path
        else:
            raise argparse.ArgumentTypeError(f'{path} is not a valid path to an SQLite Database.')

    def add_arguments (self, parser):
        def add_arguments(self, parser):
            parser.add_argument('sqlite_file', type=self._db_path)

    def handle(self, *args, **options):
        guildID = '480817692350218250'
        conn = sqlite3.connect((options['sqlite_file']))
        c = conn.cursor()

        self.stdout.write(f'- - Scanning channels')
        c.execute('SELECT userID, gameName, gameRoom, name')
        channelList = c.fetchall()
        self.stdout.write(f'- Found {len(channelList)} channels in the database.')

        for channel in channelList:
            self.stdout.write(f'- - Migrating channel {channel[2]} ({channel[1]})')
            user = User.objects.get_or_create(id=channel[3])[0]
            Channel.objects.get_or_create(id=channel[2], owner=user, guild_id=guildID, game=channel[1])
            self.stdout.write(f'- - Migrated channel {channel[2]} successfully.')
        # Migrate
        c.close()
