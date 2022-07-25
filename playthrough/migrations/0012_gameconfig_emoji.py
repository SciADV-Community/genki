# Generated by Django 4.0.6 on 2022-07-24 19:37

from django.db import migrations
import genki.models


class Migration(migrations.Migration):

    dependencies = [
        ('playthrough', '0011_guild_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameconfig',
            name='emoji',
            field=genki.models.DiscordIDField(blank=True, default=None, help_text='The custom emoji ID to use for the create channel button.', null=True),
        ),
    ]
