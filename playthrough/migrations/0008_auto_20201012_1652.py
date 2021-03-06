# Generated by Django 3.1.2 on 2020-10-12 16:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('playthrough', '0007_game_playable'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='The last time the user logged in.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(help_text="The User's Discord username.", max_length=100, null=True),
        ),
    ]
