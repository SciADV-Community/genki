from pathlib import Path
from playthrough.models import Game, GameConfig, Guild

from django.core.management import call_command

from . import PlaythroughTestBase


class TestMigrateShogun(PlaythroughTestBase):
    def test_migrate_short(self):
        db_path = Path(__file__).resolve().parents[0] / 'fixtures' / 'shogun_short.db'
        args = [str(db_path.resolve())]
        call_command('migrate_shogun', *args)
        # Check Config migration
        guilds = list(Guild.objects.all())
        assert len(guilds) == 1
        chaos_world = guilds[0]
        assert chaos_world.name == 'Chaos World'
        # Check Game migration
        games = list(Game.objects.all())
        assert len(games) == 5
        chaos_child = Game.objects.prefetch_related('aliases')\
            .select_related('completion_role').get(name='Chaos;Child')
        assert chaos_child.channel_suffix == "-plays-chaos"
        assert len(chaos_child.aliases.all()) == 3
        assert chaos_child.completion_role.name == "Chaos Child"
        # Check GameConfig migration
        cc_config = GameConfig.objects.get(guild=chaos_world, game=chaos_child)
        assert cc_config.playable
        # Check Channel migration
        channels = chaos_world.channels.all()
        assert len(channels) == 5
