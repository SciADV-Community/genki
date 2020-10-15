# Generated by Django 3.1.2 on 2020-10-14 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playthrough', '0008_auto_20201012_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='channel_suffix',
            field=models.CharField(blank=True, help_text='The suffix for channels for the game.', max_length=30),
        ),
        migrations.AlterField(
            model_name='guild',
            name='admins',
            field=models.ManyToManyField(blank=True, help_text="The Guild's bot admins.", related_name='admin_for', to='playthrough.User'),
        ),
    ]
